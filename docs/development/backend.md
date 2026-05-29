## Basic architecture of TURTL
TURTL consists of a Vue.js frontend (for a development guide, see [here](https://github.com/U2Vj/turtl/wiki/Frontend:-Getting-Started-with-Development)) and a Python backend that provides a REST API. The backend uses [Django](https://www.djangoproject.com/) and the [Django REST Framework](https://www.django-rest-framework.org/). Currently, the TURTL backend requires Python 3.10 or later.

### Libraries used
#### Django
* provides an ORM, a login system, an admin panel and more
* Docs: [https://docs.djangoproject.com/en/5.0/](https://docs.djangoproject.com/en/5.0/)

#### Django REST Framework
* provides the framework for creating REST API endpoints within Django
* Docs: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

#### Django REST Framework SimpleJWT
* provides an authentication backend for the Django REST Framework that uses JWT tokens
* For more information, see [[Authentication and Authorization]]
* Docs: [https://django-rest-framework-simplejwt.readthedocs.io/en/latest/](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

#### Django Rules
* provides object-level permissions to Django, e.g. checking whether an instructor manages a classroom (and can therefore modify/delete it)
* For more information, see [[Authentication and Authorization]]
* Docs: [https://github.com/dfunckt/django-rules/blob/master/README.rst](https://github.com/dfunckt/django-rules/blob/master/README.rst)

#### Django Channels and channels_redis
* used to handle WebSocket connections. channels_redis is a Redis channel layer backend for Django Channels.
* For more information, see [[Virtualization and Shell]]
* Docs: [https://channels.readthedocs.io/en/latest/](https://channels.readthedocs.io/en/latest/) and [https://github.com/django/channels_redis/](https://github.com/django/channels_redis/)

#### Docker SDK for Python
* Used for virtualization
* For more information, see [[Virtualization and Shell]]
* Docs: [https://docker-py.readthedocs.io/en/stable/](https://docker-py.readthedocs.io/en/stable/)

### Backend architecture
Django projects are structured into [applications](https://docs.djangoproject.com/en/5.0/ref/applications/). Each application is also a Python package. The _turtl_ folder is the project Python package which contains a settings module (_settings.py_) that defines the TURTL configuration (see [[Installation, database seeding and configuration]]). It also contains a custom exception handler and routing configurations for both ASGI (in the _routing.py_ file) and WSGI (in the _urls.py_ file). ASGI is used for asynchronous communication (e.g. WebSocket connections), WSGI for regular HTTP. TURTL only uses ASGI for the online shell (see [[Virtualization and Shell]]).

TURTL consists of five custom applications:

#### Authentication
The authentication app provides a customized User model and endpoints to login and logout a user. It also provides API endpoints to update the current user's profile, to list all instructors and administrators within TURTL and it implements the email invitation system.

URLs that are handled by the authentication app are prefixed with _/users/_.

#### Catalog
The catalog app manages the retrieval, creation, modification and deletion of classrooms, projects and tasks. Therefore, it implements most of the features that are specific to instructors and administrators. The catalog app is dependent on the authentication app because it uses the custom User model. It does not depend on the enrollments app.

URLs that are handled by the catalog app are prefixed with _/catalog/_.

#### Enrollments
The enrollments app manages enrolling students into classrooms, unenrolling them and solving tasks. Therefore, it implements most of the features that are available to students. The enrollment app is dependent on the authentication app and on the catalog app.

URLs that are handled by the enrollments app are prefixed with _/enrollments/_.

#### Seeder
The seeder app is optional and its sole purpose is to provide a Django management command called `seed`. This command can be used to seed test data into the database. For more information, see [[Installation, database seeding and configuration]]. The seeder app is dependent on the authentication app, the catalog app and the enrollments app.

#### Shell
The shell app handles virtualizations and the websocket connections for the online shell. Please see [[Virtualization and Shell]] for more information.