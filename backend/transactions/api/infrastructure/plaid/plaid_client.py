import requests
import os
from dotenv import load_dotenv

load_dotenv()


class PlaidClient:
    __base_url__ = os.getenv("plaid_base_url")
    __client_id__ = os.getenv("plaid_client_id")
    __secret__ = os.getenv("plaid_client_secret")
    __client_name__ = os.getenv("app_name")
    __products__ = [item.strip() for item in os.getenv("plaid_products").split(",")]
    __country_codes__ = [item.strip() for item in os.getenv("plaid_country_codes").split(",")]

    def create_link_token(self, client_user_id, language) -> str:
        request = {
            "client_id": self.__client_id__,
            "secret": self.__secret__,
            "user": {
                "client_user_id": f"{client_user_id}"
            },
            "client_name": self.__client_name__,
            "country_codes": self.__country_codes__,
            "products": self.__products__,
            "language": language
        }

        try:
            response = requests.post(f"{self.__base_url__}/link/token/create", json=request)

            response.raise_for_status()

            data = response.json()
            return data['link_token']
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Exception: {err}")
            raise err
