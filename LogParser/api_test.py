import requests

url = "https://bored-api.appbrewery.com/random"

try:
    response = requests.get(url)
    data = response.json()
    print("Success!")
    print(data)
except requests.exceptions.RequestException as e:
    print(f"An error occured while calling the api {e}")
    
