from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.account.serializers import RegistrationSerializer, LoginSerializer, ResetPasswordSerilizer, \
    CreateNewPasswordSerializer, ChangePasswordSerializer, PurchaseHistorySerializer, MyUserSerializer

User = get_user_model()


class UserPurchasesView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PurchaseHistorySerializer





class RegistrationApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Регистрация прошла успешно, вам было выслано эл.письмо для активации вашего аккаунта',
                            status=201)


class AccountActivationView(APIView):

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Вы успешно активировали свой аккаунт =)', status=200)
        except User.DoesNotExist:
            return Response('Неверный активационный код или вы не зарегестрированы =(', status=400)


class LoginApiView(ObtainAuthToken):
    serializer_class = LoginSerializer


class ResetPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ResetPasswordSerilizer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.send_reset_password_link()
        return Response('Вам отправлено письмо для восстановления пароля')


class CreateNewPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = CreateNewPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_pass()
        return Response('Пароль успешно восстановлен')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data,
                                               context={'request': request})

        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        return Response('Вы успешно изменили свой пароль')


class LogOutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            Token.objects.filter(user=user).delete()
            return Response('Вы вышли из своего аккаунта')
        except:
            return Response(status=403)


class MyUserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
