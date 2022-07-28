from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.purchase.models import Purchase
from apps.purchase.serializers import PurchaseSerializer
from apps.vehicle.models import Vehicle


class PurchaseView(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


class ConfirmPurchaseView(APIView):
    def get(self, request, barcode):
        try:
            vehicle = Vehicle.objects.get(barcode=barcode)
            vehicle.is_available = False
            vehicle.save()
            purchase = Purchase.objects.get(vehicle=vehicle)
            purchase.is_confirmed = True
            purchase.save()
            return Response('Вы успешно заказали vehicle!')
        except:
            return Response('Что-то не так. Покупка не прошла!')
