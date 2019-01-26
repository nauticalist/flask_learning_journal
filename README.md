# Work Log with a Database
---

Treehouse Techdegree Project 5

A personal learning journal web application with flask and peewee


## Dependencies

- Python 3.6 or later
- flask==1.0.2
- peewee==3.8.2
- Unidecode==1.0.23
- Flask-Bcrypt==0.7.1
- Flask-WTF==0.14.2

Refer to requirements.txt

## Before start

Before starting the app modify config.py file as you wish

```
DEBUG = True
PORT = 8080
HOST = '127.0.0.1'
DB_NAME = 'journal.db'
SECRET_KEY = 'rfWF1AKPS8qpJoQ3iLoG6J0bGGDAZ9Yd'
# Default admin user to be created
DEFAULT_USER = 'admin'
DEFAULT_USER_PASSWORD = 'password'
DEFAULT_USER_EMAIL = 'admin@test.com'
```

## To start

```
git https://github.com/nauticalist/flask_learning_journal.git
cd flask_learning_journal
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python app.py
```
