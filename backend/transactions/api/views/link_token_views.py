from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.infrastructure.plaid.plaid_client import PlaidClient
from rest_framework.response import Response


class LinkTokenView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_id = request.user.id
        language = request.query_params.get("lang", None)

        if user_id is None:
            return Response(status=401)
        
        if language is None:
            language = "es"

        try:
            client = PlaidClient()
            link_token = client.create_link_token(client_user_id=user_id, language=language)
            return Response({"link_token": link_token}, status=200)
        except Exception as ex:
            return Response({"message": f"{ex}"}, status=500)