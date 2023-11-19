from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('menu-items', views.menuitems),
    path('menu-items/<int:menuItem>', views.Menuitem.as_view()),
    path('groups/manager/users', views.Assign_Manager.as_view()),
    path('groups/manager/users/<int:userId>', views.Remove_manager.as_view()),
    path('groups/delivery-crew/users', views.Assign_Delivery.as_view()),
    path('groups/delivery-crew/users/<int:userId>', views.Remove_delivery.as_view()),
    path('cart/menu-items', views.cart.as_view()),
    path('orders', views.order_views),
]