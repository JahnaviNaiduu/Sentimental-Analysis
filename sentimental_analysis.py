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

# Dropdown box for both search and keyword recommendations
search_term = st.selectbox("Select a term to search or a recommended keyword", list(keyword_recommendations.keys()))
recommended_keywords = keyword_recommendations.get(search_term, [])
# Filter the dataframe based on search or recommended keyword.
# Checks if the chosen word is present in Title OR Keywords in the dataset.
#Collects only those matching rows.
m1 = df["Title"].str.contains(search_term)
m2 = df["Keywords"].str.contains(search_term)
df_search = df[m1 | m2]

#It shows results as cards in rows of 3.Each card displays an article’s info.
N_cards_per_row = 3
for n_row, row in df_search.reset_index().iterrows():
    i = n_row % N_cards_per_row
    if i == 0:
        st.write("---")
        cols = st.columns(N_cards_per_row, gap="large")

#filling each card
with cols[n_row % N_cards_per_row]:
    st.caption(f"{row['Category'].strip()} - {row['Date'].strip()} ")
    st.markdown(f"**{row['Title'].strip()}**")
    st.markdown(f"*{row['Description'].strip()}*")
    st.markdown(f"**{row['URL']}**")

#Adds a button for each article saying “Analyse”.
#If clicked, it fetches the article’s URL.
if st.button(f"Analyse_{n_row}"):
    url = row['URL']






