import os

class Config:
    # University Information
    UNIVERSITY_NAME = "Dayananda Sagar University"
    DEPARTMENT_NAME = "MBA Department"
    
    # Model Configuration
    MODEL_PATH = "./models/llama-3.2-1b.Q4_K_M.gguf"
    VECTORDB_PATH = "./vectordb"
    
    # Model Parameters
    N_CTX = 2048
    N_THREADS = 4
    MAX_TOKENS = 256
    TEMPERATURE = 0.3
    
    # Application Settings
    SECRET_KEY = os.urandom(24)
    DEBUG = True
    
    # Retrieval Settings
    TOP_K_DOCUMENTS = 3
