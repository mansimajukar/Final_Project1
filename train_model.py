import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

print("Current working directory:", os.getcwd())

# load dataset
df = pd.read_csv("dataset.csv")

X = df["url"]
y = df["label"]

print("Training started...")

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = RandomForestClassifier()
model.fit(X_vec, y)

# 🔥 FORCE SAVE IN CURRENT FOLDER
model_path = os.path.join(os.getcwd(), "model.pkl")
vectorizer_path = os.path.join(os.getcwd(), "vectorizer.pkl")

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print("Model saved at:", model_path)
print("Vectorizer saved at:", vectorizer_path)

print("Files exist:", os.path.exists(model_path), os.path.exists(vectorizer_path))