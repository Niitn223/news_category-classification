<<<<<<< HEAD
import streamlit as st
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# ---------- 1. PAGE CONFIG ----------
st.set_page_config(page_title="News Category Classifier", page_icon="📰", layout="centered")

# ---------- 2. TITLE & HEADER ----------
st.title("📰 News Category Classifier")
st.markdown("Enter a news headline below to predict its category using a machine learning model.")

# ---------- 3. TEXT CLEANING FUNCTION ----------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # remove links
    text = re.sub(r'[^a-zA-Z ]', '', text)  # keep only letters
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    return text.strip()

# ---------- 4. LOAD AND TRAIN MODEL ----------
@st.cache_data
def load_model():
    df = pd.read_csv("News_Category_Dataset.csv")  # CSV file

    # ✅ Check required columns
    if 'headline' not in df.columns or 'category' not in df.columns:
        st.error("CSV must have 'headline' and 'category' columns.")
        st.stop()

    # ✅ Filter top categories (you can modify this)
    top_categories = ['POLITICS', 'ENTERTAINMENT', 'BUSINESS', 'SPORTS', 'TECH']
    df = df[df['category'].isin(top_categories)]

    # ✅ Clean text and encode labels
    df['cleaned'] = df['headline'].apply(clean_text)
    le = LabelEncoder()
    df['label'] = le.fit_transform(df['category'])

    # ✅ Train-test split
    X_train, X_test, y_train, y_test = train_test_split(df['cleaned'], df['label'], test_size=0.2, random_state=42)

    # ✅ TF-IDF vectorizer and model
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=10000)
    X_train_vec = vectorizer.fit_transform(X_train)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    return model, vectorizer, le

model, vectorizer, le = load_model()

# ---------- 5. FRONTEND INPUT ----------
user_input = st.text_input("📝 Enter a news headline:")

if st.button("🔍 Predict Category"):
    if user_input:
        cleaned = clean_text(user_input)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]
        predicted_category = le.inverse_transform([prediction])[0]
        st.success(f"✅ Predicted Category: **{predicted_category}**")
    else:
        st.warning("Please enter a headline.")

# ---------- 6. Show All Possible Categories ----------
st.markdown("---")
st.subheader("📚 Categories Used in This Model:")
for cat in le.classes_:
    st.markdown(f"- {cat}")

=======
import streamlit as st
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# ---------- 1. PAGE CONFIG ----------
st.set_page_config(page_title="News Category Classifier", page_icon="📰", layout="centered")

# ---------- 2. TITLE & HEADER ----------
st.title("📰 News Category Classifier")
st.markdown("Enter a news headline below to predict its category using a machine learning model.")

# ---------- 3. TEXT CLEANING FUNCTION ----------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # remove links
    text = re.sub(r'[^a-zA-Z ]', '', text)  # keep only letters
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    return text.strip()

# ---------- 4. LOAD AND TRAIN MODEL ----------
@st.cache_data
def load_model():
    df = pd.read_csv("News_Category_Dataset.csv")  # CSV file

    # ✅ Check required columns
    if 'headline' not in df.columns or 'category' not in df.columns:
        st.error("CSV must have 'headline' and 'category' columns.")
        st.stop()

    # ✅ Filter top categories (you can modify this)
    top_categories = ['POLITICS', 'ENTERTAINMENT', 'BUSINESS', 'SPORTS', 'TECH']
    df = df[df['category'].isin(top_categories)]

    # ✅ Clean text and encode labels
    df['cleaned'] = df['headline'].apply(clean_text)
    le = LabelEncoder()
    df['label'] = le.fit_transform(df['category'])

    # ✅ Train-test split
    X_train, X_test, y_train, y_test = train_test_split(df['cleaned'], df['label'], test_size=0.2, random_state=42)

    # ✅ TF-IDF vectorizer and model
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=10000)
    X_train_vec = vectorizer.fit_transform(X_train)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    return model, vectorizer, le

model, vectorizer, le = load_model()

# ---------- 5. FRONTEND INPUT ----------
user_input = st.text_input("📝 Enter a news headline:")

if st.button("🔍 Predict Category"):
    if user_input:
        cleaned = clean_text(user_input)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]
        predicted_category = le.inverse_transform([prediction])[0]
        st.success(f"✅ Predicted Category: **{predicted_category}**")
    else:
        st.warning("Please enter a headline.")

# ---------- 6. Show All Possible Categories ----------
st.markdown("---")
st.subheader("📚 Categories Used in This Model:")
for cat in le.classes_:
    st.markdown(f"- {cat}")

>>>>>>> 8c59588479f5b586af1c22e4c8635cfc6214d453
