from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.infrastructure.plaid.plaid_client import PlaidClient


class TransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        client = PlaidClient()

        access_token = client.get_access_token(data["public_key"])

        transactions = client.get_transactions(
            access_token=access_token,
            start_date=data["start_date"],
            end_date=data["end_date"]
        )

        result = [{
            "amount": transaction.amount,
            "iso_currency_code": transaction.iso_currency_code,
            "category": transaction.category,
            "date": transaction.date,
            "authorized_date": transaction.authorized_date,
            "name": transaction.name,
            "merchant_name": transaction.merchant_name,
            "pending": transaction.pending
        } for transaction in transactions]

        return Response(result, status=200)




