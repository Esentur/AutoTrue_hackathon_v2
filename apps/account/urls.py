from django.urls import path

from apps.account.views import *

urlpatterns = [
    path('registration/', RegistrationApiView.as_view()),
    path('active/<uuid:activation_code>/', AccountActivationView.as_view()),
    path('login/', LoginApiView.as_view()),
]
