from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.vehicle.models import Type, Vehicle, Review, Like, Rating, Favourite
from apps.vehicle.serializers import TypeSerializer, VehicleSerializer, ReviewSerializer, RatingSerializer


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

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk, *args, **kwargs):
        try:
            fav_obj, _ = Favourite.objects.get_or_create(author=request.user, vehicle_id=pk)
            fav_obj.favourite = not fav_obj.favourite
            fav_obj.save()
        except:
            return ('The vehicle does not exits!')
        if fav_obj.favourite:
            return Response('Added to Favourites')
        return Response('Removed from Favourites')

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        try:
            like_obj, _ = Like.objects.get_or_create(author=request.user, vehicle_id=pk)
            like_obj.like = not like_obj.like
            like_obj.save()
        except:
            return ('The vehicle does not exist!')

        if like_obj.like:
            return Response('LIKED')
        return Response('UNLIKED')

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(seller=request.user, vehicle_id=pk)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data)

    def get_permissions(self):
        # print(self.action)
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'like' or self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]


class ReviewView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
