from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.core.mail import send_mail

User = get_user_model()


def send_active_mail(code, email, username):
    full_link = f'http://localhost:8000/account/active/{code}/'
    send_mail(
        "Ваш активационный код",
        f"Здравствуйте {username.title()}.\n Пожалуйста перейдите по ссылке: {full_link} \n для активации вашего аккаунта.",
        'sulimanovuran@gmail.com',
        [email]
    )


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        p = attrs.get('password')
        p2 = attrs.pop('password2')

        if p != p2:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_active_mail(code, user.email, user.username)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Нет такого пользователя')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Данные введены не корректно')
            attrs['user'] = user
            return attrs


