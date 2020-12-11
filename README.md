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