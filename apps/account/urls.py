from django.urls import path

from apps.account.views import RegistrationApiView

urlpatterns = [
    path('registration/', RegistrationApiView.as_view()),
]
