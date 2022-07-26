from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.mail import send_mail

User = get_user_model()


def send_active_mail(code, email, username):
    full_link = f'http://localhost:8000/api/v1/account/active/{code}/'
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



