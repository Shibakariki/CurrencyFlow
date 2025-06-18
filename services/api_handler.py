import requests

class APIHandler:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def fetch_exchange_rate(self, from_curr, to_curr):
        params = {
            'access_key': self.api_key,
            'source': from_curr,
            'currencies': to_curr,
        }

        response = requests.get(self.api_url, params=params)
        data = response.json()

        if response.status_code != 200 or "error" in data:
            raise Exception("Erreur lors de la récupération des taux de change.\n\n"+data["error"]["type"]+": \n"+data["error"]["info"])
        rate = data["quotes"][from_curr + to_curr]

        return rate
    
    def convert_currency(self, amount, from_curr, to_curr):
        if amount <= 0:
            raise ValueError("Le montant doit être supérieur à zéro.")
        
        rate = 2
        rate = self.fetch_exchange_rate(from_curr, to_curr)
        converted_amount = round(rate * amount, 4)
        
        return converted_amount