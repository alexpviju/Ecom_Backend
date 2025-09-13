from django.urls import path
from .views import (
    SignupView, LoginView, ForgotPasswordView,
    VerifyOTPView, ResetPasswordView, ChangePasswordView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('verify-otp/', VerifyOTPView.as_view(), name="verify-otp"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
]
