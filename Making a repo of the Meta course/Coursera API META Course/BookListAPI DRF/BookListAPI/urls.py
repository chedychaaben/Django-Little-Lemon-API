from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.books),
    path('BookList/', views.BookList.as_view()),
    path('Book/<int:pk>/', views.Book.as_view()),
]