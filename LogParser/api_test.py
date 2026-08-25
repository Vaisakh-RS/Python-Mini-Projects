import requests

class fetchApi:
    url:str

    def __init__(self):
        self.url="https://bored-api.appbrewery.com/"

    def api_fetch(self,parameter):
        try:
            api=f"{self.url}{parameter}"
            response = requests.get(api)
            if(response.status_code!=200):
                return None
            return  response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occured while calling the api - {e}")
            return None

api_call=fetchApi()
response=api_call.api_fetch("random")
print(response)
