GTM Buddy - FastAPI Application
This is a FastAPI-based application for multi-label text classification, entity extraction, and summarization. It uses a pre-trained machine learning model and spaCy for natural language processing tasks. The application is containerized using Docker for easy deployment.

Features
Multi-Label Text Classification:

Predicts labels for a given text snippet using a pre-trained model.

Entity Extraction:

Extracts entities like competitors, features, and pricing keywords using a domain knowledge base and spaCy.

Text Summarization:

Generates a summary of the input text using spaCy.

Prerequisites
Before running the application, ensure you have the following installed:

Docker: Install Docker

Python: Install Python (optional, for local development)

Setup Instructions
1. Clone the Repository
Clone this repository to your local machine:
git clone https://github.com/your-username/gtm-buddy.git
cd gtm-buddy

3. Build the Docker Image
Build the Docker image using the provided Dockerfile:
docker build -t gtm-buddy .

4. Run the Docker Container
Run the Docker container, mapping port 8000 on your host to port 8000 in the container:
docker run -d -p 8000:8000 --name gtm-buddy-container gtm-buddy

5. Access the Application
Once the container is running, you can access the application at:

Swagger UI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

Using the API
1. Predict Labels and Extract Entities
Send a POST request to the /predict endpoint with a JSON body containing the text snippet.

Example Request
Invoke-WebRequest -Uri "http://localhost:8000/predict" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"text_snippet": "We love the analytics, but CompetitorX has a cheaper subscription. Can you provide a discount? Our team is also concerned about data security."}'

Example Response:
json
{
  "predicted_labels": [1, 0, 1, 0, 0],
  "extracted_entities": {
    "competitors": ["CompetitorX"],
    "features": ["analytics"],
    "pricing_keywords": ["discount"]
  },
  "summary": "We love the analytics, but CompetitorX has a cheaper subscription."
}

2. Check API Health
You can check the health of the service by sending a GET request to the /health endpoint:
curl http://localhost:8000/health



Development Setup for locally:

1. Install Dependencies
If you want to run the application locally without Docker, install the required Python packages:
pip install -r requirements.txt
python -m spacy download en_core_web_sm


2. Run the Application Locally
Start the FastAPI server:
uvicorn app:app --reload
