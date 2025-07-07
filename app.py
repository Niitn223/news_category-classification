import streamlit as st
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="News Category Classifier", page_icon="📰", layout="centered")
st.title("📰 News Category Classifier")
st.markdown("Enter a news headline below to predict its category using a machine learning model.")

# Function to clean the input text
def clean_text(text):
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Load model and prepare data
@st.cache_data
def load_model():
    df = pd.read_csv("news_sample.csv")

    if 'headline' not in df.columns or 'category' not in df.columns:
        st.error("CSV must have 'headline' and 'category' columns.")
        st.stop()

    # Limit to 5 main categories
    top_categories = ['POLITICS', 'ENTERTAINMENT', 'BUSINESS', 'SPORTS', 'TECH']
    df = df[df['category'].isin(top_categories)]

    # ✅ Balance the dataset (100 samples per category)
    df = df.groupby('category').apply(lambda x: x.sample(n=100, random_state=42)).reset_index(drop=True)

    # Clean and encode
    df['cleaned'] = df['headline'].apply(clean_text)
    le = LabelEncoder()
    df['label'] = le.fit_transform(df['category'])

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(df['cleaned'], df['label'], test_size=0.2, random_state=42)

    # TF-IDF and model
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=10000)
    X_train_vec = vectorizer.fit_transform(X_train)
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    return model, vectorizer, le

# Load trained model
model, vectorizer, le = load_model()

# User input
user_input = st.text_input("📝 Enter a news headline:")

# Predict button
if st.button("🔍 Predict Category"):
    if user_input:
        cleaned = clean_text(user_input)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]
        predicted_category = le.inverse_transform([prediction])[0]
        st.success(f"✅ Predicted Category: **{predicted_category}**")
    else:
        st.warning("Please enter a headline.")

# Show categories
st.markdown("---")
st.subheader("📚 Categories Used in This Model:")
for cat in le.classes_:
    st.markdown(f"- {cat}")
