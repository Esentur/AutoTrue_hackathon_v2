from django.urls import path

from apps.account.views import *

urlpatterns = [
    path('registration/', RegistrationApiView.as_view()),
    path('active/<uuid:activation_code>/', AccountActivationView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('forgot_password/', ResetPasswordView.as_view()),
    path('create_new_password/', CreateNewPasswordView.as_view()),
    path('logout/', LogOutApiView.as_view()),
    path('change_password/', ChangePasswordView.as_view())
]
