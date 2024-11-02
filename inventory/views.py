from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
import logging
from .filters import InventoryFilter
from .models import Inventory
from .forms import InventoryForm, CSVUploadForm
import json
import csv
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import os

# Set up logging
logger = logging.getLogger(__name__)

def add_book(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Book added successfully.")
                return redirect('book-list')
            except Exception as e:
                logger.error(f"Error adding book: {e}")
                messages.error(request, "An error occurred while adding the book.")
    else:
        form = InventoryForm()
    return render(request, 'inventory/add_book.html', {'form': form})

@login_required
def book_list(request):
    try:
        book_filter = InventoryFilter(request.GET, queryset=Inventory.objects.all())
        return render(request, 'inventory/book_list.html', {'filter': book_filter})
    except Exception as e:
        logger.error(f"Error fetching book list: {e}")
        messages.error(request, "An error occurred while fetching the book list.")
        return render(request, 'inventory/book_list.html', {'filter': None})

def search_book(request):
    try:
        search_filter = InventoryFilter(request.GET, queryset=Inventory.objects.all())
        return render(request, 'inventory/search_book.html', {'filter': search_filter})
    except Exception as e:
        logger.error(f"Error searching for books: {e}")
        messages.error(request, "An error occurred while searching for books.")
        return render(request, 'inventory/search_book.html', {'filter': None})

def edit_book(request, id):
    book = get_object_or_404(Inventory, id=id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=book)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Book updated successfully.")
                return redirect('book-list')
            except IntegrityError:
                messages.error(request, "A database integrity error occurred while updating the book.")
            except Exception as e:
                logger.error(f"Error updating book: {e}")
                messages.error(request, "An error occurred while updating the book.")
    else:
        form = InventoryForm(instance=book)
    return render(request, 'inventory/edit_book.html', {'form': form, 'book': book})

def delete_book(request, id):
    book = get_object_or_404(Inventory, id=id)
    if request.method == 'POST':
        try:
            book.delete()
            messages.success(request, "Book deleted successfully.")
            return redirect('book-list')
        except Exception as e:
            logger.error(f"Error deleting book: {e}")
            messages.error(request, "An error occurred while deleting the book.")
    return render(request, 'inventory/delete_book.html', {'book': book})

def export_books_csv(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Author', 'Genre', 'Publication Date', 'ISBN'])
        for book in Inventory.objects.all():
            writer.writerow([book.title, book.author, book.genre, book.publication_date, book.isbn])

        return response
    except Exception as e:
        logger.error(f"Error exporting books to CSV: {e}")
        messages.error(request, "An error occurred while exporting books to CSV.")
        return redirect('book-list')

def export_books_json(request):
    try:
        books = list(Inventory.objects.values('title', 'author', 'genre', 'publication_date', 'isbn'))
        for book in books:
            if isinstance(book['publication_date'], date):
                book['publication_date'] = book['publication_date'].isoformat()

        response = HttpResponse(json.dumps(books), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="books.json"'
        return response
    except Exception as e:
        logger.error(f"Error exporting books to JSON: {e}")
        messages.error(request, "An error occurred while exporting books to JSON.")
        return redirect('book-list')

def import_books(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = request.FILES['csv_file']
                valid_extensions = {'.csv'}
                file_extension = os.path.splitext(csv_file.name)[1].lower()

                if file_extension not in valid_extensions:
                    messages.error(request, "Invalid file type. Please upload a CSV file.", extra_tags="import")
                    return render(request, 'inventory/import_books.html', {'form': form})

                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)

                headers = next(reader, None)
                if headers and headers[0].lower() == 'title':
                    reader = list(reader)

                for row in reader:
                    if len(row) < 5:
                        messages.error(request, f"Row {row} does not have enough columns.", extra_tags="import")
                        continue

                    try:
                        title, author, genre, publication_date, isbn = row
                        if Inventory.objects.filter(isbn=isbn.strip()).exists():
                            messages.warning(request, f"Book with ISBN {isbn.strip()} already exists.", extra_tags="import")
                            continue

                        Inventory.objects.create(
                            title=title.strip(),
                            author=author.strip(),
                            genre=genre.strip(),
                            publication_date=publication_date.strip(),
                            isbn=isbn.strip()
                        )
                    except IntegrityError:
                        messages.error(request, f"Could not process book with ISBN {isbn.strip()} due to a database error.", extra_tags="import")
                    except ValueError as e:
                        messages.error(request, f"Error processing row {row}: {e}", extra_tags="import")

                messages.success(request, "Books imported successfully.", extra_tags="import")
            except Exception as e:
                logger.error(f"Unexpected error during CSV import: {e}")
                messages.error(request, "An unexpected error occurred during import.")
        else:
            messages.error(request, "There was an error with the form submission.", extra_tags="import")
    else:
        form = CSVUploadForm()

    return render(request, 'inventory/import_books.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')
                return redirect('book-list')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
        except Exception as e:
            logger.error(f"Error during user login: {e}")
            messages.error(request, "An error occurred during login.")
    return render(request, 'inventory/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('login')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')
            except Exception as e:
                logger.error(f"Error during user registration: {e}")
                messages.error(request, "An error occurred during registration.")
    else:
        form = UserCreationForm()
    return render(request, 'inventory/register.html', {'form': form})
