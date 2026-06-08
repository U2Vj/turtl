## Basic architecture of TURTL
TURTL consists of a Vue.js frontend (for a development guide, see [here](https://github.com/U2Vj/turtl/wiki/Frontend:-Getting-Started-with-Development)) and a Python backend that provides a REST API. The backend uses [Django](https://www.djangoproject.com/) and the [Django REST Framework](https://www.django-rest-framework.org/). Currently, the TURTL backend requires Python 3.12 or later.

### Libraries used
#### Django
* provides an ORM, a login system, an admin panel and more
* Docs: [https://docs.djangoproject.com/en/5.0/](https://docs.djangoproject.com/en/5.0/)

#### Django REST Framework
* provides the framework for creating REST API endpoints within Django
* Docs: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

#### Django REST Framework SimpleJWT
* provides an authentication backend for the Django REST Framework that uses JWT tokens
* For more information, see [Authentication](authentication.md)
* Docs: [https://django-rest-framework-simplejwt.readthedocs.io/en/latest/](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

#### Django Rules
* provides object-level permissions to Django, e.g. checking whether an instructor manages a classroom (and can therefore modify/delete it)
* For more information, see [Authentication](authentication.md)
* Docs: [https://github.com/dfunckt/django-rules/blob/master/README.rst](https://github.com/dfunckt/django-rules/blob/master/README.rst)

#### Django Channels and channels_redis
* used to handle WebSocket connections. channels_redis is a Redis channel layer backend for Django Channels.
* Docs: [https://channels.readthedocs.io/en/latest/](https://channels.readthedocs.io/en/latest/) and [https://github.com/django/channels_redis/](https://github.com/django/channels_redis/)

#### Proxmoxer
* used to call the Proxmox VE API from the vm manager.
* Docs: [https://github.com/proxmoxer/proxmoxer/](https://github.com/proxmoxer/proxmoxer/)


### Backend architecture
Django projects are structured into [applications](https://docs.djangoproject.com/en/5.0/ref/applications/). Each application is also a Python package. The _turtl_ folder is the project Python package which contains a settings module (_settings.py_) that defines the TURTL configuration. It also contains a custom exception handler and routing configurations for both ASGI (in the _routing.py_ file) and WSGI (in the _urls.py_ file). ASGI is used for asynchronous communication (e.g. WebSocket connections), WSGI for regular HTTP.

TURTL consists of seven custom applications:

#### Authentication
The authentication app provides a customized User model and endpoints to login and logout a user. It also provides API endpoints to update the current user's profile, to list all instructors and administrators within TURTL and it implements the email invitation system.

URLs that are handled by the authentication app are prefixed with _/users/_.

#### Catalog
The catalog app manages the retrieval, creation, modification and deletion of classrooms, projects and tasks. Therefore, it implements most of the features that are specific to instructors and administrators. The catalog app is dependent on the authentication app because it uses the custom User model. It does not depend on the enrollments app.

URLs that are handled by the catalog app are prefixed with _/catalog/_.

#### Enrollments
The enrollments app manages enrolling students into classrooms, unenrolling them and solving tasks. Therefore, it implements most of the features that are available to students. The enrollment app is dependent on the authentication app, the analytics app and on the catalog app.

URLs that are handled by the enrollments app are prefixed with _/enrollments/_.

#### Seeder
The seeder app is optional and its sole purpose is to provide a Django management command called `seed`. This command can be used to seed test data into the database. It also provides commands to generate and cleanup student accounts called `generate_students` and `cleanup_students`.

For more information, see [Installation Guide](../setup/installation.md). The seeder app is dependent on the authentication app, the catalog app and the enrollments app.

#### Shell
The shell app handles the websocket connections for the noVNC shell.
The central component is the VMConsoleConsumer (a Django Channels AsyncWebsocketConsumer) which is used as a proxy between the client browser and the VNC WebSocket endpoint of Proxmox VE. This way the Proxmox host does not need to be exposed directly.

Connections are limited via the WS_MAX_PARALLEL_PER_USER environment variable which has the default value of 3. This is counted via Redis cache and prevents users from opening too many tabs to help preserve the server resources.


#### VM Manager
The VM manager app handles the creation and management of the virtualizations and lab environments by provisioning the resources on Proxmox VE.
It allows tasks to have realistic lab environments that can have one or multiple interconnected VMs.
The Proxmox logic is separated into 4 different files:

- [client.py](../../vm_manager/proxmox/client.py) handles the connection to the Proxmox API with Proxmoxer.
- [network_pool.py](../../vm_manager/proxmox/network_pool.py) handles the creation and deletion of networks for lab environments
- [orchestrator.py](../../vm_manager/proxmox/orchestrator.py) contains the functions that create, start, stop and delete lab environments as well as a function to clean up orphan VMs that exist on proxmox while missing in the database
- [vm_ops.py](../../vm_manager/proxmox/vm_ops.py) contains the underlying functions to clone and configure individual VMs as well as monitoring their status.

The VM Manager also provides a management command to cleanup unused lab environments and delete orphan VMs. It is called in deployment by the cleanup service every 10 minutes. The time after which a VM is stopped as well as the time after which a VM is deleted can be set in the .env file.
You can also call the command manually by running:

```bash
python manage.py cleanup_lab_envs
```
The app is dependent on the authentication app, the catalog app and the analytics app.

#### Analytics
The analytics app provides a data model to record various events about how users are interacting with the application. It contains a data model and a tracker function that can be called from anywhere in the TURTL app to record user events.
Currently the following events are recorded: user_login, user_logout, task_failed, task_completed, lab_stopped, lab_resumed, lab_deleted, lab_created

### Database
**PostgreSQL** has been chosen as the database because some parts of VM provisioning cannot run in parallel. Therefore the application uses PostgreSQL locking mechanism to prevent these race conditions.

**Redis** is used as a Channel layer and for websocket connection rate limiting.