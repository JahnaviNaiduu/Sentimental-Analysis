from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import newspaper
from textblob import TextBlob
from PIL import Image
import requests
from io import BytesIO
import pytesseract
import syllapy
import uvicorn

app = FastAPI(title="NLP Sentiment Analysis API", version="1.0")
origins = [
    "http://localhost:3000",     # React local dev
    "http://127.0.0.1:3000",
    "http://localhost:5173",     # Vite or alternate dev server
    "http://127.0.0.1:5173",
    "*"  # You can restrict this later for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],             # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],             # Allow all headers
)

# ---------- Load Dataset ----------
try:
    df = pd.read_csv("SearchEngine_Dataset.csv", encoding="latin1").fillna("")
except Exception as e:
    raise RuntimeError(f"Error loading dataset: {e}")

# ---------- Sentiment Analysis Function ----------
def perform_sentiment_analysis(text: str):
    """Performs sentiment and readability analysis on text."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    word_count = len(blob.words)
    complex_words = sum(1 for word in blob.words if len(word) > 3)
    syllable_per_word = sum(syllapy.count(word) for word in blob.words) / word_count if word_count > 0 else 0
    personal_pronouns = (
        blob.words.count("I") +
        blob.words.count("me") +
        blob.words.count("my") +
        blob.words.count("My")
    )
    return {
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "word_count": word_count,
        "complex_words": complex_words,
        "syllable_per_word": round(syllable_per_word, 3),
        "personal_pronouns": personal_pronouns
    }

# ---------- Extract Text from Image ----------
def extract_text_from_image_url(image_url: str):
    """Extracts text from an image URL using OCR."""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image URL: {e}")
        return None

# ---------- Request Model ----------
class AnalysisRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

# ---------- Endpoints ----------

@app.get("/get_data_pool")
def get_data_pool():
    """Return the entire dataset."""
    try:
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error returning data: {e}")

@app.post("/perform_analysis")
def perform_analysis(request: AnalysisRequest):
    """Perform sentiment analysis on given text or article/image URL."""
    if not request.text and not request.url:
        raise HTTPException(status_code=400, detail="Either 'text' or 'url' must be provided.")

    text_content = None

    # If text directly provided
    if request.text:
        text_content = request.text

    # If URL provided
    elif request.url:
        url = request.url.strip()
        try:
            if url.lower().endswith(("jpg", "jpeg", "png", "gif")):
                text_content = extract_text_from_image_url(url)
                if not text_content:
                    raise HTTPException(status_code=422, detail="Failed to extract text from image.")
            else:
                article = newspaper.Article(url)
                article.download()
                article.parse()
                text_content = article.text
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Error extracting content from URL: {e}")

    # Perform sentiment analysis
    if text_content:
        result = perform_sentiment_analysis(text_content)
        return {
            "status": "success",
            "source": "text" if request.text else "url",
            "results": result
        }
    else:
        raise HTTPException(status_code=400, detail="No valid text found for analysis.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
