from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from apps.vehicle.models import Type, Vehicle
from apps.vehicle.serializers import TypeSerializer, VehicleSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page_size'
    max_page_size = 5000


class TypeView(ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = LargeResultsSetPagination


class VehicleView(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['title', 'year', 'type', 'price']
    ordering_fields = ['title', 'id']
    search_fields = ['title']

    def perform_create(self, serializer):
        # при создании Vehicle, сохрани seller'а взяв текущего юзера
        serializer.save(seller=self.request.user)
