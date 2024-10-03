
# Django Cisco Test

This repository contains a Django project setup for testing and deployment. Follow the steps below to run the project locally.

## Prerequisites

Ensure you have the following installed on your machine:
- Python 3.x (preferably version 3.8 or higher)
- pip (Python package installer)
- virtualenv (optional but recommended for managing dependencies in isolation)
- PostgreSQL (or the database you're using)
- Git (for version control)

## Installation Guide

### 1. Clone the Repository

First, clone the repository from your version control system (e.g., GitHub):

```bash
git clone https://github.com/tibeb-dev/django-cisco-test
cd django-cisco-test
```

### 2. Set Up a Virtual Environment

It’s a good practice to use a virtual environment to isolate dependencies. To create and activate one:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment (Linux/Mac)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scriptsctivate
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up the `.env` File

Ensure you have a `.env` file at the root of your project to store environment variables. This file should include your database credentials and other sensitive information. Example `.env` file:

```bash
# MySQL environment variables
MYSQL_DATABASE=mydb
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_ROOT_PASSWORD=root
MYSQL_HOST=localhost
MYSQL_PORT=3306

# AWS S3 Bucket Name
AWS_BUCKET_NAME=your-s3-bucket
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=your-region
```

Make sure that the `.env` file is listed in `.gitignore` to prevent it from being tracked by version control.

### 5. Set Up the Database

#### a. MySQL Setup

Ensure MySQL is installed and running. Create a new database for the project:

```bash
# Log into MySQL
mysql

# Create a new database
CREATE DATABASE <database_name>;
```

Ensure that your `.env` file contains the correct database connection settings.

#### b. Run Migrations

After setting up the database, run Django migrations to create the necessary tables:

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

To create an admin account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up a username, email, and password.

### 7. Run the Django Development Server

To run the development server:

```bash
python manage.py runserver
```

By default, the server will be accessible at `http://127.0.0.1:8000/`. You can visit this URL in your web browser.

## Docker Compose

You can also run the Django project with Docker and Docker Compose for easier setup and isolation of services.

### 1. Run the Application

with the `docker-compose.yml` and `Dockerfile` up, you can build and run the application using the following command:

```bash
docker-compose up --build
```

This will start both the Django application and the MySQL database in containers. The Django app will be available at `http://localhost:8000`.

### 5. Run Database Migrations

After starting the application, you need to run the migrations to set up the database:

```bash
docker-compose exec web python manage.py migrate
```

### 8. Access the Admin Panel

If you created a superuser, you can access the Django admin panel at:

```bash
http://127.0.0.1:8000/admin/
```

Log in with your superuser credentials.


