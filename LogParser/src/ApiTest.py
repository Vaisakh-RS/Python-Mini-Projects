import requests

class fetchApi:
    url:str

    def __init__(self):
        self.url="https://bored-api.appbrewery.com/"

    def api_fetch(self,parameter): #here parameter is a local variable since it's not self.parameter
        try:
            api=f"{self.url}{parameter}"
            response = requests.get(api)
            if(response.status_code!=200):
                return None
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occured while calling the api - {e}")
            return None

