# Step 1: Installing
This project is based on Django framework, thus, in the beginning setup a Python 3.x is assumed installed. The command to install Django is: 
``` python -m pip install Django ```
To install database:
go download and install PostgreSQL https://www.postgresql.org/download/ 
To install adapter:
``` pip install psycopg2 ```
To add an admin account: 
``` python manage.py createsuperuser ```
The account is: postgres, password is: admin
In order to solve the error: RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods
Using: ``` pip install cryptography ```

# Step 2: PostgreSQL
First, ask Django to switch to use postgreSQL instead of default setting. This is done by modify the follow lines in settings.py
``` 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lucrato_catalogue_DB',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
 ```

Use pgAdmin4 to create database:
  
To migrate crated tables into PostgreSQL database:
``` python manage.py makemigrations ``` 
and 
``` python manage.py migrate ```

Now you can use command ``` python manage.py runserver ``` to start server. The website now can be seen at http://localhost:8000/ 

# Step 3: Bootstrap
In order to reduce developing time cost, Bootstrap is used as UI setting up tool. To install Bootstrap:
``` pip install django-bootstrap-v5 ```

# Step 4: Demo content adding
Before you add the content, you need to create a superuser account, use command: ``` python manage.py createsuperuser ```


