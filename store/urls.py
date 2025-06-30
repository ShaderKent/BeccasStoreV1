from django.urls import path
from .views import DetailedProductView, CategoryView, StoreView

app_name = "store"

urlpatterns = [
    path("", StoreView.as_view(), name="store"),
    path("c/<str:category_name>/", CategoryView.as_view(), name="products_by_category"),
    path("p/<str:slug>/", DetailedProductView.as_view(), name="product_details"),
]
