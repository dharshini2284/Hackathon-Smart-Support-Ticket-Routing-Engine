import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load and train once at startup
data = pd.read_csv("sample_train_data.csv")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["text"])
y = data["category"]

classifier = LogisticRegression()
classifier.fit(X, y)


def classify_ticket(text: str) -> str:
    X_input = vectorizer.transform([text])
    prediction = classifier.predict(X_input)
    return prediction[0]


def detect_urgency(text: str) -> bool:
    pattern = r"\b(ASAP|urgent|immediately|broken|critical)\b"
    return bool(re.search(pattern, text, re.IGNORECASE))