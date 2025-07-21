from django.urls import path
from accounts import views
from .views import LoginView, RegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("activate/<uidb64>/<token>", views.activate_view, name="activate"),
]
