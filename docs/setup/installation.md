# Installing dependencies and running TURTL
Please note: These guides are only suitable for development purposes, not for production deployments.

## Prerequisites
TURTL requires a recent version of [Python](https://www.python.org/) (Python 3.10 or later), [Docker](https://www.docker.com/) and the latest LTS version of [NodeJS](https://nodejs.org/en).

## Backend

1. It is highly recommended to run Python applications inside virtual environments (please refer to the [Python Documentation](https://docs.python.org/3/library/venv.html) for further explanation). To create a new virtual environment in a new folder called _venv/_, run the following command inside of the repository's root folder:
```shell
python -m venv venv
```

2. Now, enter the newly created virtual environment:
#### macOS / Linux
```shell
source ./venv/bin/activate
```
#### Windows PowerShell
```powershell
venv\Scripts\Activate.ps
```
If PowerShell returns an error, there might be an issue with your execution policy. Please refer to the [PowerShell Documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies) for additional information.
#### Windows Command Prompt (cmd.exe)
```powershell
venv\Scripts\activate.bat
```
The prompt should now begin or end with _(venv)_ to indicate that you have entered the environment.

3. Install the dependencies:
```shell
pip install -r requirements.txt
```

4. Create a database and all necessary tables:
```shell
python manage.py migrate
```

5. All users of TURTL have to be invited by others first, which is why TURTL does not come with a registration form. To have an initial account, either use the accounts provided by the database seeder (if applicable, see the section below) or create an administrator account manually using the following command:
```shell
python manage.py createsuperuser
```

6. Run the backend API with a development server:
```shell
python manage.py runserver
```

The backend API should now be accessible at http://localhost:8000.

## Frontend
1. Change into the _frontend/_ directory:
```shell
cd frontend/
```
2. Install dependencies:
```shell
npm install
```
3. Run the frontend using the [Vite](https://vitejs.dev/) development server:
```shell
npm run dev
```

## Docker
TURTL uses Docker for the virtualizations associated with the tasks. However, since TURTL still remains in the prototype phase, this feature has not been fully implementet yet. But it is possible to showcase the online shell behaviour using a single demo container of Kali Linux. When solving a task, the online shell will then always connect to the Kali Linux container, regardless of what the instructors specified in the _Virtualizations_ section of the task.

To set up this demo container, execute the following steps:

1. Make sure you are a member of the _docker_ group. You can verify this by showing the groups you are a member of using the `groups` command. If _docker_ is not in this list, add your user to the _docker_ group using the following command:
```shell
sudo usermod -aG docker $USER
```
You have to log out and back in again for the changes to take effect.

2. Start the Docker Engine:
```shell
sudo systemctl start docker
```

3. Fetch the image and run the container by executing the following command in the root folder of the repository:
```shell
sudo docker compose up -d
```

4. Find and copy the container ID of the _kalilinux/kali-rolling_ container:
```shell
sudo docker ps
```

5. Paste the ID into the _turtl/settings.py_ file, line 197:
```python
# [...]

# ID of the Kali container used to demonstrate the web shell
KALI_CONTAINER_ID = "e81db3749f0e"

# [...]
```

6. Find and copy the IP address of the Redis container:
```shell
sudo docker inspect -f  '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' turtl-redis-1
```

7. Paste it into _turtl/settings.py_, line 21:
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('REDIS_IP_ADDRESS', 6379)],
        },
    },
}
```

You should now be able to connect to the container from within a task. Please note: This guide is only suited for Linux and macOS. Windows is not supported.

# Database seeding
To ease development, TURTL provides a database seeder that fills the database with users, classrooms, projects, tasks and enrollments.

To use the database seeder, make sure the _seeder_ app is installed by checking the `INSTALLED_APPS` section of the _turtl/settings.py_ file:
```python
# [...]

INSTALLED_APPS = [
    # [...]
    'authentication',
    'catalog',
    'enrollments',
    'shell',
    'seeder'
]

# [...]
```

When the _seeder_ app is installed, the following Django management command seeds the database:
```shell
python manage.py seed
```

Clearing the database, seeding it and starting TURTL is possible by chaining the following commands:
```shell
python manage.py flush --noinput && python manage.py seed --noinput && python manage.py runserver
```

### Account credentials
The seeder inserts the following accounts into the database:
| Role | No. of accounts | Emails | Password for each account |
| ---- | --------------- | ------ | ------------------------- |
| Administrator | 1 | admin@localhost | admin |
| Instructor | 3 | instructor@localhost, instructor2@localhost, instructor3@localhost | instructor |
| Student | 5 | student@localhost, student2@localhost, student3@localhost, student4@localhost, student5@localhost | student |

# Configuration
## Backend
The backend configuration of TURTL is stored in the _turtl/settings.py_ file. Many configuration options are for [Django](https://docs.djangoproject.com/en/5.0/ref/settings/) itself, the [Django REST framework](https://www.django-rest-framework.org/api-guide/settings/), [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) or other libraries that TURTL uses. Please refer to their specific documentation for more information.

The configuration options specific to TURTL are:
| Name | Data type | Description | Example / default value |
| ---- | --------- | ----------- | ----------------------- |
| `FRONTEND_URL` | String | The URL of the TURTL frontend, without a trailing slash | `'http://localhost:5173'` |
| `INVITATION_EXPIRY_DAYS` | Integer | The number of days for which an invitation sent via TURTL's email invitation system is valid | `14` |
| `KALI_CONTAINER_ID` | String | The ID of the Kali Linux container (see above) | |

Please note: To use the email invitation system, TURTL requires an SMTP server. Further information about configuring the Django email service is provided in the [official Django documentation](https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-EMAIL_HOST). TURTL uses the default Django email backend and sends every email from the email address specified in the `DEFAULT_FROM_EMAIL` setting.

## Frontend
The frontend configuration can be customized in the _frontend/.env.development_ file. 

| Name | Data type | Description | Example / default value |
| ---- | --------- | ----------- | ----------------------- |
| `VITE_API_URL` | String | The URL of the TURTL backend API | `http://localhost:8000/` |
| `VITE_WS_URL` | String | The base URL for the Websocket connections to the TURTL backend. Required for the online shell | `ws://127.0.0.1:8000/shell` |

For development, these configuration options should not need adjusting.

# Deployment notes
The guides above are not suitable for production environments. To deploy the backend API, an ASGI server is necessary because TURTL uses asynchronous Django features. More information on this can be obtained from the [Django documentation](https://docs.djangoproject.com/en/5.0/howto/deployment/). Also, always change Django's `SECRET_KEY` and never keep it at the default development value specified in the _turtl/settings.py_ file. Furthermore, the authentication backend ([SimpleJWT](https://github.com/jazzband/djangorestframework-simplejwt)) requires a cronjob to be run regularly that will remove expired tokens from the database. This is achieved with the command `python manage.py flushexpiredtokens`.