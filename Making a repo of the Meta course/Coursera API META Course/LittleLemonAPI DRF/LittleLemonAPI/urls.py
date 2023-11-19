
from django.contrib import admin
from django.urls import path, include
from .views import MenuItemsView, SingleMenuItemsView


urlpatterns = [
    path('menu-items', MenuItemsView.as_view()),
    path('menu-items/<int:pk>/', SingleMenuItemsView.as_view()),
]
