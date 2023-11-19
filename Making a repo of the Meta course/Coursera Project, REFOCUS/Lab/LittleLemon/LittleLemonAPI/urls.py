from django.urls import path 
from . import views 
  
urlpatterns = [
    # Category
    path('category/', views.CategoryView.as_view()),
    # MenuItems
    path('menu-items/', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>/', views.MenuItemOneView.as_view()),
    path('cart/menu-items/', views.CustomerCartView.as_view()),
    # Managers
    path('groups/manager/users/', views.ManagerUsersView.as_view()),
    path('groups/manager/users/<int:pk>/', views.ManagerOneUserView.as_view()),
    # Delivery Crew
    path('groups/delivery-crew/users/', views.DeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>/', views.DeliveryOneCrewView.as_view()),

    # Orders
    path('orders/', views.OrdersView.as_view()),
    path('orders/<int:pk>/', views.OrdersOneView.as_view()),

]