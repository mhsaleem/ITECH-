Punny Django Web Application
==========

##Based around **[Django](https://www.djangoproject.com/)**! 

####To access a live version, go to: [Python Anywhere](https://rorybain.pythonanywhere.com/punny/)

To run locally:
 - Clone the repo using the url provided by Github above
 - Make sure you've set up a Virtual Environment for Punny
```
$ mkvirtualenv punny
$ workon punny
```
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
 - Then launch your browser (preferably chrome) and go to: [http://localhost:8000/punny/](http://localhost:8000/punny/)
