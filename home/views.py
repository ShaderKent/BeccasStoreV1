from django.views.generic import ListView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from category.models import Category


class HomeView (ListView):
    model = Category
    template_name = "home.html"
    context_object_name = "categories"

    def get_queryset(self, *args, **kwargs):
        #Handles pagination
        query_set = Category.objects.all()
        paginator = Paginator(query_set, 1)
        page = self.request.GET.get("page")
        paged_categories = paginator.get_page(page)
        return paged_categories
