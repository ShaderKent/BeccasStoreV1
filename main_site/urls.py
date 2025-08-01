"""
URL configuration for main_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings

from django.conf.urls.static import static
from store import urls as store_urls
from home import urls as home_urls
from carts import urls as cart_urls
from accounts import urls as accounts_urls


urlpatterns = [
    path("", include(home_urls, namespace="home")),
    path('admin/', admin.site.urls),
    path("store/", include(store_urls, namespace="store")),
    path("cart/", include(cart_urls, namespace="cart" )),
    path("accounts/", include(accounts_urls, namespace="accounts" )),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
