from data_manager_apiSpreadsheet import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager


data_manager = DataManager()
sheet_data = data_manager.get_dest_data()
# print(sheet_data)

# GETTING IATA CODES
# for city in sheet_data:
#     if city["IATA Code"] == "":
#         flightSearch = FlightSearch()
#         code = flightSearch.get_dest_code(city["City"])
#         city["IATA Code"] = code

# print(f"after iata: {sheet_data}")
# data_manager.update_dest_data()

# CREATING ALL THE FLIGHTS
flights = []
for x in range(len(sheet_data)):
    flights.append(FlightData())
    flights[x].destination_airport_code = sheet_data[x]["IATA Code"]
    flights[x].destination_city = sheet_data[x]["City"]
    flights[x].price = sheet_data[x]["Lowest Price"]


# GETTING PRICES
for flight in flights:
    flightsearch = FlightSearch()
    flightsearch.get_flight_price(flight)

for y in range(len(sheet_data)):
    if sheet_data[y]["Lowest Price"] > flights[y].price:
        sheet_data[y]["Lowest Price"] = flights[y].price

        msg = f"Low price alert! Only £{flights[y].price} to fly from {flights[y].departure_city}-{flights[y].departure_airport_code} to {flights[y].destination_city}-{flights[y].destination_airport_code}, from {flights[y].from_date} to {flights[y].to_date}."""
        if flights[y].stop_over == 1:
            msg = f"{msg} FLight has 1 stop over, via {flights[y].via_city}."

        notification_manager = NotificationManager()
        # SEND SMS TO YOUR NUMBER
        # notification_manager.send_sms(message=msg)

        users = data_manager.get_user_emails()
        # print(users)
        emails = [user["Email Address"] for user in users]
        names = [user["First Name"] for user in users]
#         print(emails, names)

        for i in range(len(emails)):
            # print(emails[i], names[i])
            notification_manager.send_email(name=names[i], mail=emails[i], message=msg)

data_manager.update_price_data()
