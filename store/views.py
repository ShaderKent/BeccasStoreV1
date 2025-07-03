from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q

from carts.models import CartItem
from carts.views import _cart_id
from store.models import Product

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

class StoreView (ListView):
    model = Product
    template_name = "store.html"
    context_object_name = "products"
    ordering = ["-created_date"] 

    #Handles pagination
    def get_queryset(self):
        query_set = Product.objects.all().filter(is_available=True)
        paginator = Paginator(query_set, 1)
        page = self.request.GET.get("page")
        paged_products = paginator.get_page(page)
        return paged_products

    
class CategoryView (ListView):
    model = Product
    template_name = "store.html"
    context_object_name = "products"
    ordering = ["-created_date"]
    
    def get_queryset(self, *args, **kwargs):
        #Handles pagination
        query_set = Product.objects.filter(category__slug__icontains=self.kwargs.get("category_name"), is_available=True,)
        paginator = Paginator(query_set, 1)
        page = self.request.GET.get("page")
        paged_products = paginator.get_page(page)
        return paged_products


class DetailedProductView (DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = "product"
    
    def get_context_data(self,**kwargs):
        context = super(DetailedProductView, self).get_context_data(**kwargs)
        current_product = Product.objects.get(slug=self.kwargs.get("slug"))
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(self.request), product=current_product).exists()
        context['in_cart'] = in_cart
        return context
    
class SearchView(ListView):
    model = Product
    template_name = "search.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = None
        if "keyword" in self.request.GET:
            keyword = self.request.GET["keyword"]
            if keyword:
                queryset = Product.objects.order_by("-created_date").filter(Q(description_full__icontains=keyword) | Q(description_short__icontains=keyword) | Q(product_name__icontains=keyword))
        # paginator = Paginator(queryset, 2)
        # page = self.request.GET.get("page")
        # paged_products = paginator.get_page(page)
        
        return queryset
    