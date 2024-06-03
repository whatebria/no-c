from django.contrib import admin
from .models import Proyecto
from django.contrib.auth.models import User

from django.core.exceptions import PermissionDenied

# Register your models here.

class Proyectos(admin.ModelAdmin):
    if User.objects.filter(groups__name='Profesor').exists():
        list_display = ('nombreProyecto', 'tema', 'cuentaConPatrocinio')
    else:
        list_display = ('nombreProyecto', 'tema')
    

admin.site.register(Proyecto)
