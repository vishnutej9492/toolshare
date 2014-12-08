# ToolShare 
ToolShare facilitates neighbors to share items.

## Prequisites

* Python 3.4
* Django 1.6

## Get source code
`$ git clone git@gitlab.com:hvaldecantos/toolshare.git`

## Please install the following dependencies
`$ pip install django-localflavor`
`$ pip install south`

## Database migration
`$ python manage.py syncdb --migrate`

After migrations are done, please run the command for loading initial data
`$ python manage.py loaddata ToolMgmt/initial_data.json`

## Run the application
`$ python manage.py runserver`

Note: Make sure you are in the root directory of django project where `manage.py` is located.

## Team
Team 5 - SWEN610 Fall semester 2014 - RIT
