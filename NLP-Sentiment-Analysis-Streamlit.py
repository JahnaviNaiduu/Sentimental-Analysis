import streamlit as st
import pandas as pd
import newspaper
from textblob import TextBlob
from PIL import Image
import requests
from io import BytesIO
import pytesseract
import syllapy

st.set_page_config(page_title="Sentiment Analysis-NLP", page_icon="📊", layout="wide")
st.title("Sentiment Analysis")

# Function to perform sentiment analysis on text
def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    word_count=len(blob.words)
    complex_words=sum(1 for word in blob.words if len(word) > 3)
    syllable_per_word = sum(syllapy.count(word) for word in blob.words) / word_count
    personal_pronouns = blob.words.count("I") + blob.words.count("me") + blob.words.count("my") + blob.words.count("My")
    return polarity, subjectivity,word_count,complex_words,syllable_per_word,personal_pronouns

# Function to extract text from an image URL using pytesseract
def extract_text_from_image_url(image_url):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error extracting text from the image URL. Error details: {e}")
        return None

# Connect to the Excel Sheet
df = pd.read_csv("SearchEngine_Dataset.csv", encoding='latin1').fillna("")

# Keyword recommendations
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

# Dropdown box for both search and keyword recommendations
search_term = st.selectbox("Select a term to search or a recommended keyword", list(keyword_recommendations.keys()))
recommended_keywords = keyword_recommendations.get(search_term, [])

# Filter the dataframe based on search or recommended keyword
m1 = df["Title"].str.contains(search_term)
m2 = df["Keywords"].str.contains(search_term)
df_search = df[m1 | m2]

# Display the filtered results
N_cards_per_row = 3
for n_row, row in df_search.reset_index().iterrows():
    i = n_row % N_cards_per_row
    if i == 0:
        st.write("---")
        cols = st.columns(N_cards_per_row, gap="large")

    with cols[n_row % N_cards_per_row]:
        st.caption(f"{row['Category'].strip()} - {row['Date'].strip()} ")
        st.markdown(f"**{row['Title'].strip()}**")
        st.markdown(f"*{row['Description'].strip()}*")
        st.markdown(f"**{row['URL']}**")

        # Add Analyse button
        if st.button(f"Analyse_{n_row}"):
            url = row['URL']

            if url.endswith(('jpg', 'jpeg', 'png', 'gif')):
                extracted_text = extract_text_from_image_url(url)
                if extracted_text:
                    polarity, subjectivity,word_counts,complex_word,syllable,personal = perform_sentiment_analysis(extracted_text)
                    #st.write("Article Text:", text)
                    st.write("Polarity:", format(polarity,".2f"))
                    st.write("Subjectivity:", format(subjectivity,".2f"))
                    df=pd.DataFrame([polarity,subjectivity,word_counts,complex_word,syllable,personal])
                    df.index = ['polarity', 'subjectivity', 'word_counts', 'complex_word', 'syllable', 'personal']
                    st.bar_chart(df)
                else:
                    st.write("Text extraction failed. Please check the image URL and try again.")
            else:
                article = newspaper.Article(url)
                article.download()
                article.parse()
                text = article.text
                polarity, subjectivity, word_counts, complex_word, syllable, personal = perform_sentiment_analysis(text)
                #st.write("Article Text:", text)
                st.write("Polarity:", format(polarity,".2f"))
                st.write("Subjectivity:", format(subjectivity,".2f"))
                df = pd.DataFrame([polarity, subjectivity, word_counts, complex_word, syllable, personal])
                df.index=['polarity', 'subjectivity', 'word_counts', 'complex_word', 'syllable', 'personal']
                st.bar_chart(df)
