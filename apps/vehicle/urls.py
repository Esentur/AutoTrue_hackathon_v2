from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.vehicle.views import TypeView,VehicleView

router = DefaultRouter()
router.register('type', TypeView)
router.register('vehicle', VehicleView)

urlpatterns = [
    path('', include(router.urls)),
]
