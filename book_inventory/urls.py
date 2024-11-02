"""
URL configuration for book_inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from inventory import views
from inventory.views import user_login, user_logout, user_register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add/', views.add_book, name='add-book'),
    path('', views.book_list, name='book-list'),
    path('search/', views.search_book, name='search-book'),
    path('edit/<int:id>/', views.edit_book, name='edit-book'),
    path('delete/<int:id>/', views.delete_book, name='delete-book'),
    path('export/csv/', views.export_books_csv, name='export-csv'),
    path('export/json/', views.export_books_json, name='export-json'),
    path('import/', views.import_books, name='import-books'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
]
