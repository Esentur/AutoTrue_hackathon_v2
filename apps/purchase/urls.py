from rest_framework.routers import DefaultRouter

from apps.purchase.views import PurchaseView

router = DefaultRouter()
router.register('', PurchaseView)

urlpatterns = []
urlpatterns.extend(router.urls)
