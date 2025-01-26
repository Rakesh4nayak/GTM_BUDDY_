# app.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer
import joblib
import re

# Load the dataset
df = pd.read_csv("calls_dataset.csv")

# Preprocess the text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text

df["text_snippet"] = df["text_snippet"].apply(preprocess_text)

# Encode labels
df["labels"] = df["labels"].apply(lambda x: x.split(", "))
mlb = MultiLabelBinarizer()
labels_encoded = mlb.fit_transform(df["labels"])

# Split data
X = df["text_snippet"]
y = labels_encoded

# Train the model
tfidf = TfidfVectorizer(max_features=5000)
model = Pipeline([
    ("tfidf", tfidf),
    ("clf", OneVsRestClassifier(LogisticRegression()))
])
model.fit(X, y)

# Save the model
joblib.dump(model, "multi_label_classifier.pkl")

# Load the pre-trained model
model = joblib.load("multi_label_classifier.pkl")

# FastAPI app code
from fastapi import FastAPI
from pydantic import BaseModel
import spacy

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

# Rest of the FastAPI code...
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import spacy
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
import joblib

# Load pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

# Load domain knowledge
with open("domain_knowledge.json", "r") as f:
    domain_knowledge = json.load(f)

# Load pre-trained multi-label classification model
model = joblib.load("multi_label_classifier.pkl")

# Initialize FastAPI app
app = FastAPI()

# Define input schema
class Snippet(BaseModel):
    text_snippet: str

# Dictionary Lookup
def dictionary_lookup(text):
    extracted_entities = {
        "competitors": [],
        "features": [],
        "pricing_keywords": []
    }

    for competitor in domain_knowledge["competitors"]:
        if competitor.lower() in text.lower():
            extracted_entities["competitors"].append(competitor)

    for feature in domain_knowledge["features"]:
        if feature.lower() in text.lower():
            extracted_entities["features"].append(feature)

    for keyword in domain_knowledge["pricing_keywords"]:
        if keyword.lower() in text.lower():
            extracted_entities["pricing_keywords"].append(keyword)

    return extracted_entities

# NER with spaCy
def extract_entities_with_spacy(text):
    doc = nlp(text)
    extracted_entities = {
        "competitors": [],
        "features": [],
        "pricing_keywords": []
    }

    matcher = spacy.matcher.PhraseMatcher(nlp.vocab)
    for label, phrases in domain_knowledge.items():
        patterns = [nlp(phrase) for phrase in phrases]
        matcher.add(label, None, *patterns)

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id]
        extracted_entities[label].append(span.text)

    return extracted_entities

# Combine extracted entities
def combine_extracted_entities(dict_entities, spacy_entities):
    combined_entities = {
        "competitors": list(set(dict_entities["competitors"] + spacy_entities["competitors"])),
        "features": list(set(dict_entities["features"] + spacy_entities["features"])),
        "pricing_keywords": list(set(dict_entities["pricing_keywords"] + spacy_entities["pricing_keywords"]))
    }
    return combined_entities

# Generate summary
import spacy
from spacy.lang.en import English

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def generate_summary(text, max_sentences=2):
    """
    Generate a summary by extracting the first `max_sentences` sentences.
    """
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    summary = " ".join(sentences[:max_sentences])
    return summary

# API endpoint
@app.post("/predict")
def predict(snippet: Snippet):
    text = snippet.text_snippet

    # Predict labels
    predicted_labels = model.predict([text])[0]

    # Extract entities
    dict_entities = dictionary_lookup(text)
    spacy_entities = extract_entities_with_spacy(text)
    extracted_entities = combine_extracted_entities(dict_entities, spacy_entities)

    # Generate summary
    summary = generate_summary(text)

    return {
        "predicted_labels": predicted_labels.tolist(),
        "extracted_entities": extracted_entities,
        "summary": summary
    }