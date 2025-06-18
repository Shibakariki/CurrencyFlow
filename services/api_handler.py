import requests
class APIHandler:
    def __init__(self, api_url, api_key, storage):
        self.api_url = api_url
        self.api_key = api_key
        self.storage = storage

    def fetch_supported_currencies(self):
        params = {
            'access_key': self.api_key
        }

        try:
            response = requests.get(self.api_url+"/list", params=params)
            data = response.json()
            if "success" in data and data["success"] == True and "currencies" in data:
                return list(data["currencies"].keys())
            else:
                raise Exception("Erreur lors de la récupération des devises supportées")
        except requests.exceptions.RequestException as e:
            raise Exception("Erreur de connexion à l'API : " + str(e))

    def fetch_exchange_rate(self, from_curr, to_curr):
        params = {
            'access_key': self.api_key,
            'source': from_curr,
            'currencies': to_curr,
        }

        try:
            response = requests.get(self.api_url+"/live", params=params)
            data = response.json()

            rate = data["quotes"][from_curr + to_curr]
        except requests.exceptions.RequestException as e:
            #check dans l'historique si on a déjà ce taux
            history = self.storage.load_history()
            for record in history:
                if record["from"] == from_curr and record["to"] == to_curr:
                    rate = record["rate"]
                    break
            else:
                raise Exception("Erreur de connexion à l'API et pas de taux trouvé dans l'historique")
        except Exception as e:
            # raise Exception("Erreur lors de la récupération des taux de change : " + str(e))
            raise Exception("Erreur lors de la récupération des taux de change")

        return rate
    
    def convert_currency(self, amount, from_curr, to_curr):
        if amount <= 0:
            raise ValueError("Le montant doit être supérieur à zéro.")
        
        rate = self.fetch_exchange_rate(from_curr, to_curr)
        converted_amount = round(rate * amount, 4)
        
        return rate, converted_amount