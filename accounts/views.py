from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, View
from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import RegistrationForm
from accounts.models import Account

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
        user.is_active = True
        user.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful.")
        return redirect("accounts:register")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Registration unsuccessful; Please try again.")
        return response

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