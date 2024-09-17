import os

from amadeus import Client, ResponseError
from dotenv import load_dotenv

load_dotenv()
amadeus = Client(
    client_id= os.environ['AMADEUS_API_KEY'],
    client_secret=os.environ['AMADEUS_API_SECRET']
)

try:

    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='SYD', destinationLocationCode='BKK', departureDate='2024-11-20', adults=1)
    print(response.data)
except ResponseError as error:
    raise error
