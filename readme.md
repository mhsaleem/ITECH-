Punny Django Web Application
==========

##Based around **[Django](https://www.djangoproject.com/)**! 

####To access a live version, go to: [Python Anywhere](https://rorybain.pythonanywhere.com/punny/)

######To see the content used in the ITECH Presentations, see the folder ```PlanningStages```

#####To run locally:
 - Clone the repo using the url provided by Github above
```
$ git clone https://github.com/mhsaleem/ITECH-.git Punny
```
 - cd into the root directory
```
$ cd Punny
```
 - Make sure you've set up a Virtual Environment for Punny
```
$ mkvirtualenv punny
$ workon punny
```
 - Once inside the project root--and using your virtual environment--run the commands:
```
$ pip install -r requirements.txt
$ cd itech/
$ python manage.py makemigrations punny
$ python manage.py migrate
$ python populate_punny.py
$ python manage.py runserver
```
 - Then launch your browser (preferably chrome) and go to: [http://localhost:8000/punny/](http://localhost:8000/punny/)
