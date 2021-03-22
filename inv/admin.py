from django.contrib import admin
from .models import *

admin.site.register([Producto, Categoria, SubCategoria, UnidadMedida, Marca])

# Register your models here.
