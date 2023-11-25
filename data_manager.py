import requests
import os

Sheety_API_ENDPOINT = "https://api.sheety.co/daee2bd4fbe4d80a33353bf438c3fb55/myFlightDeals/prices"
Sheety_HEADERS = {
    "Authorization": os.environ.get("AUTHORIZATION")  # Get your authorization from sheety api
}


class DataManager:
    def __init__(self):
        self.dest_data = {}

    def get_dest_data(self):
        get_response = requests.get(url=Sheety_API_ENDPOINT, headers=Sheety_HEADERS)
        get_response.raise_for_status()
        data = get_response.json()
        print(data)
        self.dest_data = data["prices"]
        return self.dest_data

    def update_dest_data(self):
        for city in self.dest_data:
            body = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            put_response = requests.put(url=f"{Sheety_API_ENDPOINT}/{city['id']}", json=body, headers=Sheety_HEADERS)
            print(put_response.text)

    def update_price_data(self):
        for city in self.dest_data:
            body = {
                "price": {
                    "lowestPrice": city["lowestPrice"]
                }
            }
            put_response = requests.put(url=f"{Sheety_API_ENDPOINT}/{city['id']}", json=body, headers=Sheety_HEADERS)
            print(put_response.text)
