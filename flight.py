import os
import requests
import pycountry
import airportsdata
from dotenv import load_dotenv

# load end data.
load_dotenv()
KEY_ID = os.getenv('AMADEUS_API_KEY')
KEY_SECRET = os.getenv('AMADEUS_API_SECRET')
END_POINT = os.getenv('FLIGHT_SEARCH_API')

def get_iata_airport(city_name:str, country:str) -> dict:
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


def get_flight_data(origin:str, destination:str, departure_date:str, return_date:str, adults:int, children:int = 0,
                    infants: int = 0, travel_class:str = "ECONOMY", include_airlines:str = None,
                    exclude_airlines:str = None, nonStop:bool = False, currentCode:str = "AUD",
                    max_price:int = None, max_result:int = 20):
    """
    This function give flight fare data by using given parameters.
    :param origin: city/airport IATA code from which the traveller will depart.
    :param destination: city/airport IATA code to which the traveler is going, e.g. PAR for Paris
    :param departure_date: the date on which the traveler will depart from the origin to go to the destination.
                            Dates are specified in the ISO 8601 YYYY-MM-DD format, e.g. 2017-12-25
    :param return_date: the date on which the traveler will depart from the destination to return to the origin.
                        If this parameter is not specified, only one-way itineraries are found.
    :param adults: the number of adult travelers (age 12 or older on date of departure).
    :param children: the number of child travelers (older than age 2 and younger than age 12 on date of departure)
                    who will each have their own separate seat. If specified, this number should be greater than or
                    equal to 0.
    :param infants: the number of infant travelers (whose age is less or equal to 2 on date of departure).
                    Infants travel on the lap of an adult traveler, and thus the number of infants must not
                     exceed the number of adults. If specified, this number should be greater than or equal to 0
    :param travel_class: most of the flight time should be spent in a cabin of this quality or higher.
                        The accepted travel class is economy, premium economy, business or first class.
                        If no travel class is specified, the search considers any travel class.
    :param include_airlines: This option ensures that the system will only consider these airlines.
                        This can not be cumulated with parameter excludedAirlineCodes.
    :param exclude_airlines: This option ensures that the system will ignore these airlines.
                            This can not be cumulated with parameter includedAirlineCodes.
    :param nonStop: if set to true, the search will find only flights going from the origin to the destination with no stop in between
    :param currentCode: the preferred currency for the flight offers. Currency is specified in the ISO 4217 format
    :param max_price: maximum price per traveler. By default, no limit is applied. If specified, the value should be a positive number with no decimals
    :param max_result: maximum number of flight offers to return. If specified, the value should be greater than or equal to 1
    :return: dictionary object of response.
    """

    if not any([origin, destination, departure_date, return_date, adults, children, infants, travel_class,
                include_airlines, exclude_airlines, nonStop, currentCode, max_price, max_result]):
        return {"is_successful":False, "response":"Please enter all the required arguments and try again."}

    # get list of airports in both origin and destination city in iata code.
    origin_airports_iata = [airport['iata'] for airport in get_iata_airport(city_name=origin, country= "Australia")['response']]
    destination_airports_iata = [airport['iata'] for airport in get_iata_airport(city_name=destination, country="Australia")['response']]

    # remove all black from origin and destination airport list.
    origin_airports_iata = [airport for airport in origin_airports_iata if airport != '']
    destination_airports_iata = [airport for airport in destination_airports_iata if airport != '']

    origin_airports_iata = origin_airports_iata[0]
    destination_airports_iata = destination_airports_iata[0]

    # Set up headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Prepare the data for the POST request
    data = {
        "grant_type": "client_credentials",
        "client_id": KEY_ID,
        "client_secret": KEY_SECRET
    }

    try:
        # Send POST request to the API
        response = requests.post(url=os.getenv('ACCESS_TOKEN_ENDPOINT'), headers=headers, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            access_token =  {"is_successful": True, "token": response.json()}
        else:
            access_token =  {"is_successful": False, "error": response.json()}

    except requests.exceptions.RequestException as e:
        access_token =  {"is_successful": False, "error": str(e)}

    # check if access token is successfully retrieved.
    if access_token['is_successful']:
        access_token = access_token['token']['access_token']

    else:
        raise "No access token, try again"



    # Set up headers with authorization
    headers = {
        'Authorization': f'Bearer {access_token}',  # Replace with your actual access token
        'Content-Type': 'application/json'
    }

    params = {
        'originLocationCode': origin_airports_iata,
        'destinationLocationCode': destination_airports_iata,
        'departureDate': departure_date,
        # 'returnDate': return_date,
        'adults': 1,
        #'children': children,
        #'infants': infants,
        #'travelClass': travel_class,
        #'includedAirlineCodes': include_airlines,
        #'excludedAirlineCodes': exclude_airlines,
        #'nonStop': nonStop,
        #'currencyCode': currentCode,
        #'maxPrice': max_price,
        #'max': max_result
    }

    response = requests.get(url=END_POINT, json=params, headers=headers)

get_flight_data("Brisbane", "Melbourne", "2024-10-25", return_date=None, adults=1)