# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files for Django
RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for Django
ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Run Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
