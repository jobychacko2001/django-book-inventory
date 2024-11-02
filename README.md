# Book Inventory Application

Welcome to the Book Inventory Application! This project helps users manage their book collection with a user-friendly interface. It allows users to add, edit, delete, and view books easily.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Integration](#api-integration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- User authentication with login and registration.
- Admin panel for managing the book inventory.
- Add, edit, and delete books.
- View detailed information about each book.
- Search and filter books.
- Responsive design with Bootstrap.

## Technologies Used

- Python
- Django
- HTML/CSS
- Bootstrap
- SQLite (for the database)
- JavaScript (for client-side interactivity)
- jQuery
- DataTables (for enhanced table features)

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/jobychacko2001/django-book-inventory
2. Navigate to the project directory:
   ```bash
   cd django-book-inventory
3. Create a virtual environment:
   ```bash
   python -m venv .venv
4. **Activate the virtual environment:**
   - For Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
6. Run the migrations:
   ```bash
   python manage.py migrate
7. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
8. Start the development server:
   ```bash
   python manage.py runserver
9. Open your web browser and go to `http://127.0.0.1:8000/` to access the application.


## Usage

After setting up the application, you can use the following features:

1. **Login**: 
   - Navigate to the login page.
   - Enter your credentials to access the application.\
     ![image](https://github.com/user-attachments/assets/c2f6c91b-eaa9-4509-ac9b-add20e250087)

2. **Admin Panel**: 
   - Access the admin panel at `/admin`.
   - Manage books directly, including adding, editing, and deleting entries.
     

3. **Book Management**: 
   - To add a new book:
     - Click on "Add Book" in the navbar.
       ![image](https://github.com/user-attachments/assets/1eba742a-d887-42f5-9be4-ac174b0ceb69)

     - Fill out the required fields such as Title, Author, ISBN, and Description.
   - To edit an existing entry, select the book and click "Edit."
     ![image](https://github.com/user-attachments/assets/1ce16237-72d9-4a2a-85bb-4f7f73af64a1)

   - To delete a book, click the "Delete" button next to the book entry.
     ![image](https://github.com/user-attachments/assets/9d63fbbe-878c-416d-8cd4-f1e7632facbd)


4. **Search Functionality**: 
   - Use the search box located at the top of the books list.
   - Enter keywords related to the book title or author to find specific books quickly.
     ![image](https://github.com/user-attachments/assets/407ac7e0-9f00-4d6c-a2a9-a60f8c4539ab)



## Contact

For any questions or feedback, please contact me at:

1. **Email:** jobychacko2001@gmail.com  
2. **GitHub:** jobychacko2001




