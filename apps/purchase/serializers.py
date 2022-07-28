from django.core.mail import send_mail
from rest_framework import serializers
from apps.purchase.models import Purchase


def send_confirmation_mail(code, email, username):
    full_link = f'http://localhost:8000/purchase/buy/{code}/'
    send_mail(
        "Подтверждение покупки",
        f"Здравствуйте {username.title()}.\n Пожалуйста перейдите по ссылке: {full_link} \n для подтверждения покупки.",
        'esenturdildebekov8@gmail.com',
        [email]
    )


class PurchaseSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source='buyer.email')

    class Meta:
        model = Purchase
        fields = '__all__'

    def create(self, validated_data):
        vehicle = validated_data['vehicle']
        barcode = vehicle.barcode
        email = validated_data['buyer']
        username = email.username
        send_confirmation_mail(barcode, email, username)
        return super().create(validated_data)


