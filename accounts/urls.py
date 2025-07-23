from django.urls import path
from accounts import views
from .views import DashboardView, LoginView, RegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("activate/<uidb64>/<token>", views.activate_view, name="activate"),
    path("forgot_password/", views.forgot_password_view, name="forgot_password"),
    path("reset_password_validate/<uidb64>/<token>", views.reset_password_validate, name="reset_password_validate"),
    path("reset_password/", views.reset_password_view, name="reset_password"),

]
