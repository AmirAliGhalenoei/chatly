from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.UserLoginView.as_view(), name="login_page"),
    path("login-verify/",views.UserLoginVerify.as_view(), name="verify_page"),
    path("register/",views.UserRegisterView.as_view(), name="register_page"),
    path("register-verify/",views.UserRegisterVerifyView.as_view(), name="register_verify_page"),
    path("resend-otp/",views.ResentOtpView.as_view(), name="resend_otp"),
    path("register-resend-otp/",views.ResentOtpRegisterView.as_view(), name="register_resend_otp"),
    path("logout/",views.UserLogoutView.as_view(), name = "logout")
]