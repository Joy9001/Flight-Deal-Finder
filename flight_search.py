import os
import requests
from datetime import datetime, timedelta
from flight_data import FlightData

TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")  # Use your own api key from tequila api
TEQUILA_API_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_HEADER = {
    "apikey": TEQUILA_API_KEY,
}
DATE_FROM = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
DATE_TO = (datetime.now() + timedelta(days=6 * 30)).strftime("%d/%m/%Y")


class FlightSearch:
    def get_dest_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city"
        }
        get_response = requests.get(url=f"{TEQUILA_API_ENDPOINT}/locations/query", headers=TEQUILA_HEADER,
                                    params=params)
        code = get_response.json()["locations"][0]["code"]
        return code

    def get_flight_price(self, flight_data: FlightData):
        params = {
            "fly_from": flight_data.departure_airport_code,
            "fly_to": flight_data.destination_airport_code,
            "date_from": DATE_FROM,
            "date_to": DATE_TO,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "curr": "GBP",
            "max_stopovers": 0,
        }
        search_response = requests.get(url=f"{TEQUILA_API_ENDPOINT}/v2/search", headers=TEQUILA_HEADER, params=params)
        search_data = search_response.json()
        # print(search_data)
        results = search_data["_results"]
        if results >= 1:
            min_price = search_data["data"][0]["price"]
            index = 0
            for i in range(results):
                min_price = min(min_price, search_data["data"][i]["price"])
                index = i
            if flight_data.price > min_price:
                flight_data.price = min_price
                flight_data.from_date = search_data["data"][index]["route"][0]["local_departure"].split("T")[0]
                flight_data.to_date = search_data["data"][index]["route"][1]["local_departure"].split("T")[0]
                flight_data.stay_period = search_data["data"][index]["nightsInDest"]
        else:
            params["max_stopovers"] = 2
            search_response = requests.get(url=f"{TEQUILA_API_ENDPOINT}/v2/search", headers=TEQUILA_HEADER,
                                           params=params)
            search_data = search_response.json()
            results = search_data["_results"]
            if results >= 1:
                min_price = search_data["data"][0]["price"]
                index = 0
                for i in range(results):
                    min_price = min(min_price, search_data["data"][i]["price"])
                    index = i
                if flight_data.price > min_price:
                    flight_data.price = min_price
                    flight_data.from_date = search_data["data"][index]["route"][0]["local_departure"].split("T")[0]
                    flight_data.to_date = search_data["data"][index]["route"][1]["local_departure"].split("T")[0]
                    flight_data.stay_period = search_data["data"][index]["nightsInDest"]
                    flight_data.stop_over = 1
                    flight_data.via_city = search_data["data"][index]["route"][0]["cityTo"]
