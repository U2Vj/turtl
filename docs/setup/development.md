# Local development guide

## Prerequisites
TURTL requires a recent version of [Python](https://www.python.org/) (Python 3.12 or later), [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/install/linux/) and the latest LTS version of [NodeJS](https://nodejs.org/en).
For the virtualization features TURTL requires an Instance of [Proxmox VE](https://www.proxmox.com/en/products/proxmox-virtual-environment/overview) connected to a network that the machine running TURTL has access to.


For local development a separate docker-compose.yaml is provided in the root of the project. This will start Redis and PostgreSQL development containers.

### Backend

1. Copy the .env.development file and set the correct values for Proxmox.
```bash
cp .env.development .env
```
Note that PROXMOX_VERIFY_SSL will not work in local development and must be left disabled as the certificate is fetched via docker secrets in production.

2. Start the PostgreSQL and Redis Container (make sure to set the required environment variables listed above)

```bash
sudo docker compose up -d
```

3. It is highly recommended to run Python applications inside virtual environments (please refer to the [Python Documentation](https://docs.python.org/3/library/venv.html) for further explanation). To create a new virtual environment in a new folder called _venv/_, run the following command inside of the repository's root folder:
```shell
python -m venv venv
```

4. Now, enter the newly created virtual environment:
#### macOS / Linux
```shell
source ./venv/bin/activate
```
#### Windows PowerShell
```powershell
venv\Scripts\Activate.ps1
```
If PowerShell returns an error, there might be an issue with your execution policy. Please refer to the [PowerShell Documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies) for additional information.
#### Windows Command Prompt (cmd.exe)
```powershell
venv\Scripts\activate.bat
```
The prompt should now begin or end with _(venv)_ to indicate that you have entered the environment.

5. Install the dependencies:
```shell
pip install -r requirements.txt
```

6. Create a database and all necessary tables:
```shell
python manage.py migrate
```

7. All users of TURTL have to be invited by others first, which is why TURTL does not come with a registration form. To have an initial account, either use the accounts provided by the database seeder (if applicable, see the section below) or create an administrator account manually using the following command:
```shell
python manage.py createsuperuser
```

8. Run the backend API with a development server:
```shell
python manage.py runserver
```

### Frontend

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

### Database Seeding

To ease development, TURTL provides a database seeder that fills the database with users, classrooms, projects, tasks and enrollments.

The following Django management command seeds the database:
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