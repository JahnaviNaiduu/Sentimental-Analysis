from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class SentimentResponse(BaseModel):
    polarity: float
    subjectivity: float
    word_counts: int
    complex_words: int
    syllable_per_word: float
    personal_pronouns: int

class SentimentRequest(BaseModel):
    url:str

def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    word_count=len(blob.words)
    complex_words=sum(1 for word in blob.words if len(word) > 3)
    syllable_per_word = sum(syllapy.count(word) for word in blob.words) / word_count
    personal_pronouns = blob.words.count("I") + blob.words.count("me") + blob.words.count("my") + blob.words.count("My")
    return polarity, subjectivity,word_count,complex_words,syllable_per_word,personal_pronouns

def extract_text_from_image_url(image_url):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error extracting text from the image URL. Error details: {e}")
        return None

df = pd.read_csv("SearchEngine_Dataset.csv", encoding='latin1').fillna("") #encoding=“Read special letters correctly.”

# Keyword recommendations for dropdown
keyword_recommendations = {
    "Climate": ["Climate Change", "Climate Science", "Climate Policy", "Climate Global warming","Climate Solution"],
    "Global": ["Global Warming", "Happening Climate Change", "Global Effect", "Global Poverty"],
    "Poverty": ["Poverty violence", "Homeless Poverty", "Poverty as"],
    "Poverty as violence":["Poverty violence", "Homeless Poverty", "Poverty as"],
    "Mental": ["Mental Health","Murder News","Kindness","Anxiety","Depression","Happiness"],
    "Health": ["Mental Health","Happy","Lived","Self Care","Happiness"],
    "Corruption": ["Duty","Corruption as cancer","Discrimination","Social"],
    "News": ["Sports News","Murder News","Insecurity","Criminal","Killing"],
    "Disaster": ["Flood","Pollution"]
}

@app.get("/getpost/")
def get_all_posts():
     return {"data":df}

@app.post("/products/")
def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return {"message": "Product created successfully", "product": product}

