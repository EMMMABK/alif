# Alif Project

## Table of Contents
1. [Overview](#overview)
2. [Project Setup](#project-setup)
   - [Requirements](#requirements)
   - [Installation](#installation)
   - [Database Setup](#database-setup)
3. [API Endpoints](#api-endpoints)
4. [Models and Serializers](#models-and-serializers)
5. [Views](#views)
6. [Routes](#routes)
7. [Documentation](#documentation)

## 1. Overview
The "Authorization Alif" project is a Django application designed for user authentication, user management, email confirmation, password management, and news management using Django and Django REST framework.

## 2. Project Setup
### Requirements
Before you begin, ensure you have the following installed on your system:
- Python
- Django
- Python packages listed in `requirements.txt`

### Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/EMMMABK/authorization-alif.git
   ```
2. Navigation
   ```bash
   cd authorization-alif
   ```
3. Install the required packages
   ```bash
   pip install -r requirements.txt
   ```
## 3. DataBase SetUp
By default, this project uses SQLite as the database. You can change the database settings in settings.py.
* Apply database migrations:
```bash
python manage.py migrate
```
* Create a superuser for admin access:
```bash
python manage.py createsuperuser
```
* Start the development server:
```bash
python manage.py runserver
```
## 4. API Endpoints
The project provides the following API endpoints:

* User Authentication and Management
   * POST /api/login/: User login.
   * POST /api/register/: User registration.
   * POST /api/email-confirmation/: Email confirmation.
   * POST /api/password-change/: Password change.
   * POST /api/password-reset/: Password reset.
   * PUT /api/user/update/<int:pk>/: Update user profile.
   * GET /api/users/: Get a list of users.
   * GET /api/user/<int:pk>/: Get user details.
* News Management
   * GET /api/news/: Get a list of news.
   * POST /api/news/create/: Create news.
   * GET /api/news/<int:pk>/: Get news details.
   * PUT /api/news/<int:pk>/: Update news.
   * DELETE /api/news/<int:pk>/: Delete news.

## 5. Models and Serializers
### User Model
* The User model represents a user in the application.
* Fields include: email, name, surname, phone_number, is_active, is_staff, password, and more.
* Serializers: UserSerializer, UserRegistrationSerializer, EmailConfirmationSerializer, PasswordChangeSerializer, PasswordResetSerializer, UserUpdateSerializer, UserFilterSerializer.

### News Model
* The News model represents a news article.
* Fields include: image, title, content, and created_at.
* Serializers: NewsSerializer, NewsCreateSerializer.

## 6. Views
Views in this project handle the logic for API endpoints. Important views include user authentication, registration, email confirmation, password management, and news management.

## 7. Routes
URL routes are defined in urls.py. They map views to specific endpoints and HTTP methods.

## 8. Documentation
For detailed API documentation, see the official Django REST framework documentation. You can also refer to the comments within the code for more information on each API endpoint's usage.

Please note: It's important to keep your SECRET_KEY and other sensitive information secure, especially in a production environment.

Feel free to customize this README.md to suit your project's specific requirements, and add any additional information or instructions as necessary.


Make sure to replace ```bash"https://github.com/EMMMABK/authorization-alif.git"``` with the actual URL of your project's repository if it's hosted on a platform like GitHub. Additionally, customize any other parts of the README to match your project's specific needs.



