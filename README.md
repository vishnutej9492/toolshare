# ToolShare 

ToolShare facilitates neighbors to share items.


Prequisites
===> Python 3.4
===> Django 1.6

Get Source code:
$ git clone git@gitlab.com:hvaldecantos/toolshare.git

Please install the following dependencies:
$ pip install django-localflavor
$ pip install south

For migration, execute: 
$ python manage.py syncdb --migrate

After migrations are done, please run the command for loading initial data
$ python manage.py loaddata ToolMgmt/initial_data.json

And finally,run the application:
$ python manage.py runserver

Team 5 
