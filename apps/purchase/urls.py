from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.purchase.views import PurchaseView, ConfirmPurchaseView

router = DefaultRouter()
router.register('', PurchaseView)

urlpatterns = [
    path('buy/<uuid:barcode>/', ConfirmPurchaseView.as_view())
]
urlpatterns.extend(router.urls)
