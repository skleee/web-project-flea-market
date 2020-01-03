from django.urls import path
from . import views

urlpatterns = [
    path('<product_id>/', views.detail, name='detail'),
    path('<product_id>/bid/', views.bid, name='bid'),

    # Buyer
    path('<product_id>/addwish/', views.addwish, name='addwish'),
    path('<product_id>/buy/', views.buy, name='buy'),
    path('<product_id>/review', views.review, name='review'),

    # Seller
    path('<product_id>/delete', views.deleteProduct, name='delete'),
    path('<product_id>/modify', views.modifyProduct, name='modify'),
    path('<product_id>/history', views.history, name='history'),
    path('<product_id>/endauction', views.endauction, name='endauction'),

]
