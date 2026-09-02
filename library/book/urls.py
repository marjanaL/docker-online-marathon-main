from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.all_books, name='all_books'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/user/<int:user_id>/', views.user_books, name='user_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
]