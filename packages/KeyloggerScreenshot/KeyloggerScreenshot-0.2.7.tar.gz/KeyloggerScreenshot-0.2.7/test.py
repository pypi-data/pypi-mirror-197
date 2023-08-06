import requests
import time

while True:
    try:
        response = requests.get("https://www.google.com")
        print(response)
        break

    except requests.exceptions.ConnectionError:
        print("No connection")