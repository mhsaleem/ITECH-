Punny Django Web Application
==========

Based around **[Django](https://www.djangoproject.com/)**! 

To get going:
 - Clone the repo using the url provided by Github above
 - Make sure you've set up a Virtual Environment for Punny
 - Once inside of your virtual environment run the commands:

```
$ cd [root_of_project]
$ pip install -r requirements.txt
$ cd itech/
$ python manage.py makemigrations punny
$ python manage.py migrate
$ python populate_punny.py
$ python manage.py runserver
```
