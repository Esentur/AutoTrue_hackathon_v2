from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.serializers import RegistrationSerializer


class RegistrationApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Регистрация прошла успешно, вам было выслано эл.письмо для активации вашего аккаунта', status=201)

