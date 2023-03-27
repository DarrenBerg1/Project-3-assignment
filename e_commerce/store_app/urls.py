from django.urls import path
from . import views



urlpatterns = [

    path('', views.home, name='home'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('tee_shirts/', views.tee_shirts, name='tee_shirts'),
    path('hoodies/', views.hoodies, name='hoodies'),
    path('update_item/', views.update_item, name='update_item'),
    path('product/<int:id>/', views.product_by_id, name='product_detail'),
    path('search/', views.search, name='search'),
]