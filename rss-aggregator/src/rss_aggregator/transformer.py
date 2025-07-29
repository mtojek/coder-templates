from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

keyword_extractor = KeyBERT(model="all-MiniLM-L6-v2")
embedder = SentenceTransformer("all-MiniLM-L6-v2")