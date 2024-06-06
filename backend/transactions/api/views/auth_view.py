from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from api.serializers.register_serializer import RegisterSerializer


class AuthView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

        