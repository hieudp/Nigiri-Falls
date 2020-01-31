# ![](static/home/Logo.png)

# Introduction

## [Website](http://nigirifalls.herokuapp.com/)
## [GitLab](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-49)
## [Wiki](https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-49/wikis/home)


<!--![Heroku](https://heroku-badge.herokuapp.com/?app=nigirifalls)-->
![Heroku](https://img.shields.io/badge/heroku-deployed-brightgreen.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Contributors](https://img.shields.io/badge/contributors-6-brightgreen.svg)
![Linting](https://img.shields.io/badge/linting-Pylint-brightgreen.svg)


Nigiri Falls is a take-away sushi restaurant, with the possibility to order online.
Users can also create accounts, view past orders, customise their account and rate their order.
Staff can add dishes, edit availability and send messages to users.

# Prerequisites

- Python 3.7.0
- pip 19.0.3

# Installation

Navigate to the root directory, and run this command to install Django and necessary dependencies:

```
pip install -r requirements.txt
```

# Usage

### Hosting

The project is setup to be hosted at [Heroku](https://www.heroku.com/).
To use another host, remove the last line in `nigirifalls/settings.py` (django-heroku) and setup the database connection.
Also add the IP to the list of allowed_hosts.

### Commands

Make sure to to be in the root directory before running any commands.


##### Start a local server:
```
python manage.py runserver
```

##### Create admin user:
```
python manage.py createsuperuser
```

##### Create new app:
```
python manage.py startapp APPNAME
```

##### Run tests:
```
python manage.py test
```

Refer to [Django-admin and manage.py](https://docs.djangoproject.com/en/2.1/ref/django-admin/) for more commands.

### Database

SQLite3 is used for local testing by default in Django.
Edit the database field in `nigirifalls/settings.py` to change.

### Developing

1. Create a new app with the command.
2. Add the new app to the list in `nigirifalls/settings.py`
3. Add root a root url in `nigirifalls/urls.py`
4. Add sub-urls in `APPNAME/urls.py`, and direct them to view functions in `APPNAME/views.py`
5. Render HTML files stored in `templates/APPNAME`
6. Run a local server and connect with a browser at `localhost:8000`
7. Manage the database at `localhost:8000/admin`

# Folder Structure

- `nigirifalls`: Settings and root urls.
- `static`: Images, css and other files.
- `templates`: HTML files with a subfolder for each app.
- `APPNAME`: Always contains `urls.py`, `apps.py` and `views.py`. Can also contain other django modules.
