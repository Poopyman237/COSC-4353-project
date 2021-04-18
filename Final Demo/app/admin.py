from django.contrib import admin

# Register your models here.
from app.models import State, Profile

admin.site.register(State)
admin.site.register(Profile)