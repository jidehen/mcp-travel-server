import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Duffel API endpoint and key
DUFFEL_API_URL = "https://api.duffel.com/air/offer_requests"
DUFFEL_API_KEY = os.getenv("DUFFEL_ACCESS_TOKEN") 