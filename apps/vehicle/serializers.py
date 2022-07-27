from rest_framework import serializers

from apps.vehicle.models import Type, Vehicle, Image


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if not instance.type_parent:
            representation.pop('type_parent')
        return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

    seller = serializers.ReadOnlyField(source='seller.username')
    images = ImageSerializer(many=True, read_only=True)

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        vehicle = Vehicle.objects.create(**validated_data)
        # при создании vehicle создаются и записи в таблице Images
        for image in images.getlist('images'):
            Image.objects.create(vehicle=vehicle, image=image)
        return vehicle
