# Project File Structure

## manage.py

- used as an admin interface for the project after the project has been created using the django-admin commands.
- So instead of using django-admin, use 'python manage.py (command) (command arguments)' once the project has been created
  
## app (project level directory)

- it was created with the 'django-admin startproject (project_name)' command.
- \_\_init\_\_.py is an empty file that tells the python interpreter that this directory is a package.
- settings.py is the most important file. It manages the project's applications, middleware applications, database specification, and other settings of the project
- urls.py contains all of the endpoints that are a part of the website.
- asgi.py stands for Asynchronous Server Gateway Interface and is used for server deployment.
- wsgi.py stands for Web Server Gateway Interface and it is used for server deployment.

## storefront (application directory)

- it was created with the 'python manage.py startapp (application name)' command.
- \_\_init\_\_.py tells the python interpreter that this directory is a package
- admin.py is used to register models, create superuser, and log in.
- apps.py includes the application configuration for the app. Most of the time the default configuration is fine.
- models.py defines the structure of the database using classes. Includes things like database desing, relationships between data sets, and attribute constraints.
- views.py provides an interface for all of the views in forms of classes.
- tests.py used for writing test cases