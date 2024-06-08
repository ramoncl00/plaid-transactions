import requests
import os
import datetime
from dotenv import load_dotenv
from api.infrastructure.plaid.dtos.transaction_dto import Transaction

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

    def get_access_token(self, public_token) -> str:
        request = {
            "client_id": self.__client_id__,
            "secret": self.__secret__,
            "public_token": public_token
        }

        try:
            response = requests.post(f"{self.__base_url__}/item/public_token/exchange", json=request)

            response.raise_for_status()

            data = response.json()
            return data['access_token']
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Exception: {err}")
            raise err

    def get_transactions(self, access_token, start_date: str, end_date: str) -> [Transaction]:
        request = {
            "client_id": self.__client_id__,
            "secret": self.__secret__,
            "access_token": access_token,
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            response = requests.post(f"{self.__base_url__}/transactions/get", json=request)

            response.raise_for_status()

            data = response.json()

            transactions = [Transaction(
                amount=transaction["amount"],
                iso_currency_code=transaction["iso_currency_code"],
                category=transaction["category"],
                date=transaction["date"],
                authorized_date=transaction["authorized_date"],
                name=transaction["name"],
                merchant_name=transaction["merchant_name"],
                pending=transaction["pending"]
            ) for transaction in data['transactions']]

            return transactions

        except requests.exceptions.HTTPError as err:
            print(f"HTTP Exception: {err}")
            raise err