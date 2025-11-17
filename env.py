import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "app": {
        'port': os.getenv("PORT"),
    },
    "db": {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_DATABASE"),
        "pool_size": int(os.getenv("POOL_SIZE")) | 8,
        "max_overflow": int(os.getenv("MAX_OVERFLOW")) | 16,
        "pool_recycle": int(os.getenv("POOL_RECYCLE")),
    },
    "jwt": {
        "expired_in": int(os.getenv("JWT_EXPIRATION_DELTA")) | 24, # hour
        "algorithm": os.getenv("JWT_ALGORITHM"),
        "secret_key": os.getenv("JWT_SECRET"),
    },
    "google": {
        "api_key": os.getenv("GOOGLE_API_KEY"),
    },
    "elastic": {
        "url": os.getenv("ELASTIC_URL"),
        "api_key": os.getenv("ELASTIC_API_KEY")
    }
}