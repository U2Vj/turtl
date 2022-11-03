# Django
This TURTL Prototyp uses [Django](https://www.djangoproject.com/) as a Backend and [Docker](https://www.docker.com/) for managing containers.  
[*Docker SDK for Python*](https://docker-py.readthedocs.io/en/stable/) is used to call the Docker API via Django.  
The structure looks like:   
Vue.js <--> Django <--> *Docker SDK for Python* <--> Docker API  
[Django Channels](https://channels.readthedocs.io/en/latest/) is used to handle the incoming Websocket request from the Vue.js Frontend.


## Setup  
Django is a Python based Web-Framework, therefore Python3 is required and needs to be installed.  
So download and install the latest [Python3](https://www.python.org/downloads/) version.  
Django can be setup in two different ways:   
 
1.Using [Venv](https://docs.python.org/3/library/venv.html) (recommended):  
 - Venv is an alias for "virtual environment".
 - If you use venv and install some dependencies, they will not conflict with other python projects, because
 they will be installed in a new separate context.
 - Once the venv is created ```python3 -m venv /path/to/new/virtual/environment``` activated ```./path/to/new/virtual/environment/bin/activate```, all dependencies can be installed using [pip](https://pip.pypa.io/en/stable/):   
 ```pip3 install -r requirements.txt```   
 
2.Without Venv (not recommended):
 - All dependencies can be installed into the global Python package context like:  
 ```pip3 install -r requirements.txt```

## Structure
Django uses a component/app based approach to structure a web application.  
So TURTL has some components/apps like authentication, classroom, dockerService and turtl.
Each component/app capsules their own functions. So the app authentication, handles all 
functions to authenticate a user for the backend. This is a separation of concerns.
To create a new component/app use the command:   
```python manage.py startapp loremIpsum```  
The newly created app need to be registered in the turtl base components ```settings.py```.  
Todo so, add the name of the new app to the ```INSTALLED_APPS``` section.
The turtl app, is the root component/app of this Django application.  
So all new components/apps and urls must be registered at this root app.

## Developing a new component/app
To understand what each file of the newly created app does, check out the ```authentication```  
app, all files inside this app contain a little description.
## Migrating
If new models a defined or changed inside a ```models.py``` you need to create 
a migration table to map the changes to the database. To do so, run the command: ```python manage.py makemigrations```
to create the migrations and then run ```python manage.py migrate``` to apply the migrations.  
If you get the error ```django.db.utils.OperationalError: no such table: xy``` take the following actions:  
- Delete your database ```db.sqlite3``` file in your project directory.  
- Remove everything from ```__pycache__``` and ```migrations```folderss under your project subdirectorys.
- Run the command ```python manage.py makemigrations``` followed by ```python manage.py migrate --run-syncdb```.

## Admin Dashboard
URL: http://localhost:8000/admin/login  
To add an administrator Django account you have to enter the following commands in the backend terminal  
```python manage.py createsuperuser```

## Start Development-Server
Once everything is ready to be tested, you can start a local dev server with the command:   
```python manage.py runserver```

## Documentation
For a further and wider documentation, check out the official [Django documentation](https://docs.djangoproject.com/en/3.1/).
