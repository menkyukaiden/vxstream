# Register your models here.
from django.contrib import admin

from app.models import Satellites, InterfaceConfiguration, InterfaceProprieties

admin.site.register(Satellites)
admin.site.register(InterfaceConfiguration)
admin.site.register(InterfaceProprieties)