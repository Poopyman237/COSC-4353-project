To run the webpage please type in: python manage.py runserver

To run the unit test report: $ python -m coverage run manage.py test -v 2

To run the coverage report:

python -m coverage run --source='.' manage.py test app
python -m coverage html --include=app/*.*


from django.contrib.auth import authenticate, login, logout

Allow Signup and Login Using Django and diifrentiate the diffrent types
of Users


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

to handle the creation of new users. It has three fields namely username,
password1 and password2 (for password confirmation)


from django.shortcuts import render, redirect

Django shortcut functions Combines a given template with a given context
dictionary and returns an HttpResponse object with that rendered text.

from django.test import TestCase, RequestFactory

Unit test cases



