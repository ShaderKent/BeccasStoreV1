from django.views.generic import ListView
from .models import Product

class StoreView (ListView):
    model = Product
    template_name = "store.html"
    context_object_name = "products"
    ordering = ["-created_date"] 
    queryset = Product.objects.all().filter(is_available=True)

class CategoryView (ListView):
    model = Product
    template_name = "store.html"
    context_object_name = "products"
    ordering = ["-created_date"]
    
    def get_queryset(self, *args, **kwargs):
        # if self.kwargs.get("category_name", None):
        return Product.objects.filter(category__slug__icontains=self.kwargs.get("category_name"), is_available=True)
        # else: