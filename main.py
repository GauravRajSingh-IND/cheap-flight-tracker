import os
from dotenv import load_dotenv

# load end data.
load_dotenv()
KEY_ID = os.getenv('AMADEUS_API_KEY')
KEY_SECRET = os.getenv('AMADEUS_API_SECRET')



