from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View
from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import RegistrationForm
from accounts.models import Account

#Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from accounts.tokens import account_activation_token, password_reset_token
from django.core.mail import EmailMessage


# Create your views here.
class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = ""

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context
    
    def form_valid(self, form):
        user = Account.objects.create_user(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                username=form.cleaned_data["email"].split("@")[0],
                password=form.cleaned_data["password"],
        )
        # user.is_active = True
        user.save()


        #User Activation
        current_site = get_current_site(self.request)
        mail_subject = "Please activate your account."

        #Passes a HTML template for the creation of an email. 
        #   User data is passed in to allow for dyanamic content.
        #   A token and uid are used to allow for secure communication
        message = render_to_string("accounts/account_verification_email.html", {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        }) 
        to_email = user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
    
        messages.success(self.request, "Thank you for registering with us.")
        messages.success(self.request, "An email has been sent your email address, please click the provided link to activate your account.")
        return redirect("accounts:register")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Registration unsuccessful; Please try again.")
        return response

def activate_view(request, uidb64, token):
    # When the activation email is confirmed
    try:
        #Decode uid from passed in uidb64
        uid = urlsafe_base64_decode(uidb64).decode()
        #Query user object based off uid
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    #If user exists, activate user
    # if user is not None and default_token_generator.check_token(user, token):
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations, your account is activated.")
        return redirect("accounts:login")
    else:
        messages.error(request, "Invalid activation link.")
        return redirect("accounts:register")
    

class LoginView(TemplateView):
    template_name = "accounts/login.html"

    def post(self, request):
        if request.method == 'POST':
            email = request.POST["email"]
            password = request.POST["password"]

            user = auth.authenticate(email=email, password=password)
            
            if user is not None:
                auth.login(self.request, user)
                return redirect("store:store")
            else:
                messages.error(self.request, "Invalid login credentials.")
                return redirect("accounts:login")
                
        else:
            messages.error(self.request, "Invalid login credentials.")
            return redirect("accounts:login")

@login_required(login_url = "accounts:login")
def logout_view(request):
    auth.logout(request)
    messages.success(request, "You are now logged out.")
    return redirect("accounts:login")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            #Password reset email
            current_site = get_current_site(request)
            mail_subject = "Reset your password."

            message = render_to_string("accounts/reset_password_email.html", {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": password_reset_token.make_token(user),
            }) 
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset email has been sent your email address.")
            return redirect("accounts:login")
        else:
            messages.error(request, "Email is not associated with an account. Please try again")
            return redirect("accounts:forgot_password")
    return render(request, "accounts/forgot_password.html")

def reset_password_validate(request, uidb64, token):
    # When the activation email is confirmed
    try:
        #Decode uid from passed in uidb64
        uid = urlsafe_base64_decode(uidb64).decode()
        #Query user object based off uid
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    #If user exists, activate user
    # if user is not None and default_token_generator.check_token(user, token):
    if user is not None and password_reset_token.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password.")
        return redirect("accounts:reset_password")
    else:
        messages.error(request, "Expired password reset link, please request another.")
        return redirect("accounts:login")
    
def reset_password_view(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful.")
            return redirect("accounts:login")
        else:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:reset_password")
    else:
        return render(request, "accounts/reset_password.html")
