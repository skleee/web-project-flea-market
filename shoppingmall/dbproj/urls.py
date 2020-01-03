from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
import shop.views
import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shop.views.home, name='home'),

    path('filter/<str:f>/<str:select>', shop.views.filter, name='filter'),
    path('searchitem/', shop.views.searchitem, name='search'),

    # For buyer
    path('mypage/', shop.views.mypage, name='mypage'),
    path('wish/', shop.views.viewwish, name='viewwish'),
    path('cart/', shop.views.cart, name='cart'),

    # For seller
    path('productlist/', shop.views.productlist, name='productlist'),
    path('productregister/', shop.views.productregister, name='productregister'),

    path('shop/', include('shop.urls')),
    path('accounts/', include('accounts.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)