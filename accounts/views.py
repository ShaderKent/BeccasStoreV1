from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from django.contrib import messages
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
        user.save()
        messages.success(self.request, "Registration successful.")
        return redirect("accounts:register")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Registration unsuccessful; Please try again.")
        return response

        # return super(RegisterView, self).form_valid(form)

    
class LoginView(TemplateView):
    template_name = "accounts/login.html"

    

class LogoutView(TemplateView):
    pass