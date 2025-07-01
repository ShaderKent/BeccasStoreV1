from django.views.generic import ListView, TemplateView

from carts.models import Cart

class CartView (TemplateView):
    model = Cart
    template_name = "cart.html"
    context_object_name = "carts"
    ordering = ["-created_date"]