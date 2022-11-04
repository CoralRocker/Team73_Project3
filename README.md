# Project File Structure

## manage.py

- used as an admin interface for the project after the project has been created using the django-admin commands.
- So instead of using django-admin, use 'python manage.py (command) (command arguments)' once the project has been created

### Available subcommands

- Type 'manage.py help \<subcommand\>' for help on a specific subcommand.

#### [auth]

- changepassword
- createsuperuser

#### [contenttypes]

- remove_stale_contenttypes

#### [debug_toolbar]

- debugsqlshell

#### [django]

- check
- compilemessages
- createcachetable
- dbshell
- diffsettings
- dumpdata
- flush
- inspectdb
- loaddata
- makemessages
- makemigrations
- migrate
- optimizemigration
- sendtestemail
- shell
- showmigrations
- sqlflush
- sqlmigrate
- sqlsequencereset
- squashmigrations
- startapp
- startproject
- test
- testserver

#### [sessions]

- clearsessions
  
#### [staticfiles]

- collectstatic
- findstatic
- runserver
  
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
- models.py defines the structure of the database using classes. Includes things like database design, relationships between data sets, and attribute constraints.
- views.py provides an interface for all of the views in forms of classes.
- tests.py used for writing test cases
- urls.py an array of endpoints that are contained within the application and that can be inherited by the project level directory

## accounts (application directory)

- similar structure to storefront directory
- used for log in, log out, and sign up functionality

## templates

- This is where html files go

## static

- Contains directories for css and js files

## Pipfile / Pipfile.lock

- These files are used by pipenv
- You can install pipenv by typing 'pip install pipenv' in your terminal. You do not need to import it to your project.
- These files are used to keep track of project dependencies/requirements and are an alternative to keeping a 'requirements.txt' file.
- \[packages\] are python packages that will be used by everyone using the application
- \[dev-packages\] are python packages that are only used for developing the application.
- You can use these files by typing "pipenv install" and all of the dependencies will be installed from Pipfile.lock

## requirements.txt

- This is an inferior file to Pipfile/Pipfile.lock that keeps track of project dependencies/requirements
- You can use this file by typing "pip install -r requirements.txt" and it will install all of the packages specified in the file.