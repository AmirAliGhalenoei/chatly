from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import (
    UserLoginForm, 
    UserLoginVerifyForm,
    UserRegisterForm,
    UserRegisterVerifyForm
)
from .utils import OTP
from .models import User
from django.contrib.auth import login, authenticate, logout
# Create your views here.

# User Login View
class UserLoginView(View):
    template_name = "accounts/login.html"
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form":self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone"]
            code = OTP.send_otp_for_user(phone)
            request.session["user_info"] = {
                "phone":phone,
                "code":code
            }
            return redirect("verify_page")

        return render(request, self.template_name, {"form":form})

class UserLoginVerify(View):
    template_name = "accounts/verify_login.html"
    form_class = UserLoginVerifyForm

    def setup(self, request, *args, **kwargs):
        self.get_session = request.session.get("user_info")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        user_session = self.get_session
        if not user_session:
             return redirect("login_page")

        elif request.user.is_authenticated:
            return redirect("home")
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form":self.form_class, "phone":self.get_session["phone"]})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = self.get_session

        if form.is_valid():
            code = form.cleaned_data["code"]
            is_verify = OTP.verify_otp(user_session["phone"], code)
            if is_verify:
                user = get_object_or_404(User, phone = user_session["phone"])
                login(request, user)
                del request.session["user_info"]
                return redirect("home")

            form.add_error("code", "کد وارد شده صحیح نیست یا منقضی شده")
        return render(request, self.template_name, {"form":form, "phone":user_session["phone"]})


# User Register Views
class UserRegisterView(View):
    template_name = "accounts/register.html"
    form_class = UserRegisterForm

    def get(self, request):
        return render(request, self.template_name, {"form":self.form_class})

    def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect("home")
            return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            OTP.send_otp_for_user(cd["phone"])
            request.session["user_register_info"] = {
                "phone":cd["phone"],
                "username":cd["username"],
            }
            return redirect("register_verify_page")
        return render(request, self.template_name, {"form":form})

class UserRegisterVerifyView(View):
    template_name = "accounts/register_verify.html"
    form_class = UserRegisterVerifyForm

    def setup(self, request, *args, **kwargs):
        self.get_session = request.session.get("user_register_info")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.get_session:
            return redirect("login_page")

        elif request.user.is_authenticated:
            return redirect("home")
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        phone = self.get_session["phone"]
        return render(request,self.template_name, {"form":self.form_class, "phone":phone})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            code = form.cleaned_data["code"]
            verify = OTP.verify_otp(self.get_session["phone"], code)

            if verify:
                user = User.objects.create_user(
                    phone = self.get_session["phone"],
                    username = self.get_session["username"],
                    email = None,
                    password = None
                )
                del request.session["user_register_info"]
                login(request, user)
                return redirect("home")
            form.add_error("code", "کد وارد شده صحیح نیست یا منقضی شده")

        return render(request, self.template_name, {'form':form, "phone":self.get_session["phone"]})

# Resend Otps
class ResentOtpView(View):
    def get(self, request):
        user_session = request.session.get("user_info")
        if not user_session:
            return redirect("login_page")
        else:
            OTP.resend_otp(user_session["phone"])
            return redirect("verify_page")
        
class ResentOtpRegisterView(View):
    def get(self, request):
        user_session = request.session.get("user_register_info")
        if not user_session:
            return redirect("login_page")
        else:
            OTP.resend_otp(user_session["phone"])
            return redirect("register_verify_page")

class UserLogoutView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login_page")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        return redirect("login_page")