# E-commerce Product API

This is a Backend E-commerce Product API built using Django and Django REST Framework (DRF). The API is designed to manage products in an e-commerce platform, providing CRUD operations for products, user authentication, search functionality, and pagination.

## Features

- **Product Management (CRUD)**: Create, Read, Update, and Delete products.
- **User Authentication**: Users need to be authenticated to manage products.
- **Search Functionality**: Search for products by name or category.
- **Product Filters**: Filter products by category, price range, and stock availability.
- **Pagination**: Pagination for product listings and search results.

## Endpoints

- **GET /products/**: List all products.
- **POST /products/**: Create a new product.
- **GET /products/{id}/**: Retrieve a single product by ID.
- **PUT /products/{id}/**: Update a product by ID.
- **DELETE /products/{id}/**: Delete a product by ID.
- **GET /categories/**: List all categories.
- **POST /categories/**: Create a new category.
- **GET /users/**: List all users (admin only).
- **POST /users/**: Create a new user.
- **Authentication**: Use JWT tokens for secure API access.

## Requirements

- Python 3.13.0
- Django==5.1.4
- django-filter==24.3
- djangorestframework==3.15.2
- djangorestframework_simplejwt==5.4.0
- sqlparse==0.5.3

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/Ahmedabdelhady-tech/ecommerce_project.git
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run migrations:
    ```bash
    python manage.py migrate
    ```
4. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- **Admin panel**: You can access the Django admin panel at `http://127.0.0.1:8000/admin` to manage users, products, and categories.
- **Authentication**: To interact with protected endpoints, authenticate using JWT tokens.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
