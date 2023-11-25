import requests

API_ENDPOINT = "https://api.apispreadsheets.com/data/woWNre5vzIzsX7e6/"
EMAILS_API_ENDPOINT = "https://api.apispreadsheets.com/data/NnTd9CuO9DoDWymu/"


class DataManager:
    def __init__(self):
        self.dest_data = {}
        self.customer_data = {}

    def get_dest_data(self):
        get_response = requests.get(url=API_ENDPOINT)
        get_response.raise_for_status()
        data = get_response.json()
        # print(f"data me: {data}")
        self.dest_data = data["data"]
        return self.dest_data

    def update_dest_data(self):
        for city in self.dest_data:
            body = {
                "data": {
                    "City": city["City"],
                    "IATA Code": city["IATA Code"],
                    "Lowest Price": city["Lowest Price"]
                },
                "query": f"select * from woWNre5vzIzsX7e6 where City = '{city['City']}'"
            }
            # print(body)
            put_response = requests.post(url=API_ENDPOINT, json=body)
            put_response.raise_for_status()
            print(put_response.text)

    def update_price_data(self):
        for city in self.dest_data:
            body = {
                "data": {
                    "City": city["City"],
                    "IATA Code": city["IATA Code"],
                    "Lowest Price": city["Lowest Price"]
                },
                "query": f"select * from woWNre5vzIzsX7e6 where City = '{city['City']}'"
            }
            put_response = requests.post(url=API_ENDPOINT, json=body)
            put_response.raise_for_status()
            print(put_response.text)

    def get_user_emails(self):
        email_resp = requests.get(url=EMAILS_API_ENDPOINT)
        email_resp.raise_for_status()
        email_data = email_resp.json()
        # print(email_data)
        self.customer_data = email_data["data"]
        return self.customer_data
