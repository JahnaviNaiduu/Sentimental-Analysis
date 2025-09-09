#import the tools
import streamlit as st
import pandas as pd
import newspaper
from textblob import TextBlob
from PIL import Image # help us fetch and open images from the internet
import requests    # help us fetch and open images from the internet
from io import BytesIO  # help us fetch and open images from the internet
import pytesseract
import syllapy  #counts how many syllables are in words

#setting up
st.set_page_config(page_title="Sentiment Analysis-NLP", page_icon="📊", layout="wide") #browser tab
st.title("Sentiment Analysis") #for webpage

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