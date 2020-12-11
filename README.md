# Install

### 1. Install pipenv and activate
```
pip3 install pipenv

cd project_name/

pipenv shell

pipenv install
```

### 2. Make migrations and migrate
```
cd messenger/

./manage.py makemigrations

./manage.py migrate

./manage.py runserver
```

### 3. Host should be run

frontend -> `http://127.0.0.1:3000`

backend -> `http://127.0.0.1:8000`
