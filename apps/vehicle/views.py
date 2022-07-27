from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.vehicle.models import Type, Vehicle, Review
from apps.vehicle.serializers import TypeSerializer, VehicleSerializer, ReviewSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page_size'
    max_page_size = 5000


class TypeView(ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAdminUser]


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


class ReviewView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
