# services/embedding_service.py

from sentence_transformers import SentenceTransformer

def load_model():
    global model
    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded")

def get_embedding(text):
    return model.encode(text)