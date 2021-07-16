from django.contrib import admin
from .models import User, Permission

admin.site.register(Permission)
admin.site.register(User)