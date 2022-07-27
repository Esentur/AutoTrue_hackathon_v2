from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from apps.vehicle.models import Type, Vehicle
from apps.vehicle.serializers import TypeSerializer, VehicleSerializer


class TypeView(ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class VehicleView(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # при создании Vehicle, сохрани seller'а взяв текущего юзера
        serializer.save(seller=self.request.user)
