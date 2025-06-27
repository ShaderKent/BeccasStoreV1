from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.StoreView.as_view(), name="store"),
    path("c/<str:category_name>/", views.CategoryView.as_view(), name="products_by_category"),
]
