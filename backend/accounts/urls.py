from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    ForgotPasswordView,
    ResetPasswordView,
    ChangePasswordView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    #POST http://127.0.0.1:8000/api/auth/token/
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #  POST http://127.0.0.1:8000/api/auth/forgot-password/
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    # POST http://127.0.0.1:8000/api/auth/reset-password/
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    # POST http://127.0.0.1:8000/api/auth/change-password/  (needs login token)
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]