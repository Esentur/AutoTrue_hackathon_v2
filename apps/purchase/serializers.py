from rest_framework import serializers
from apps.purchase.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source='buyer.email')

    class Meta:
        model = Purchase
        fields = '__all__'

    def create(self, validated_data):
        vehicle = validated_data['vehicle']
        availability = vehicle.is_available

        if availability:
            vehicle.is_available = False
            vehicle.save()
        else:
            raise serializers.ValidationError('Запрашиваемый транспорт не доступен для заказа сейчас!')
        return super().create(validated_data)

