from django.views.generic import ListView

from category.models import Category


class HomeView (ListView):
    model = Category
    template_name = "home.html"
    context_object_name = "categories"
    queryset = Category.objects.all()