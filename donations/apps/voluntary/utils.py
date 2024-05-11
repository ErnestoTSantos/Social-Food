import requests
import os

class Validate:

    @staticmethod
    def verify_cep(cep: str):
        url = f"https://brasilapi.com.br/api/cep/v1/{cep}"
        resquest_api = requests.get(url=url)

        if resquest_api.status_code != 200:
            return False

        informations = resquest_api.json()
        return informations