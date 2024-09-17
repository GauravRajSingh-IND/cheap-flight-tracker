import os
import pycountry
import airportsdata
from dotenv import load_dotenv

# load end data.
load_dotenv()
KEY_ID = os.getenv('AMADEUS_API_KEY')
KEY_SECRET = os.getenv('AMADEUS_API_SECRET')
END_POINT = os.getenv('FLIGHT_SEARCH_API')


# TODO: Get IATA code from city name.
def get_iata_code(city_name:str, country:str) -> dict:
    """
    This function takes two arguments, city and country name and give the list of  airports in the city.
    :param city_name:  name of the city
    :param country: name of the country
    :return: dict of response
    """

    # Convert country name to country code.
    country_code = pycountry.countries.get(name= country)

    if not country_code:
        return {"status": False, "response" : "invalid country name provided"}

    # Load data of all airports
    try:
        airports = airportsdata.load()
    except Exception as e:
        return {"status": False, "response": f"Error while loading airport data: {str(e)}"}

    # empty list, this list is used in the response.
    airport_list = [
        airport for airport in airports.values()
        if (airport['country'] == country_code.alpha_2 or airport['country'] == country_code.alpha_3)
           and airport['city'].lower() == city_name.lower()
    ]

    if not airport_list:
        return {"status": False, "response": "No airports found for the given city and country."}

    return {"status": True, "response": airport_list}
