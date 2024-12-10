from django.contrib import admin
from .models import Tipo, Venta, Producto, Detalle,Local

admin.site.register(Tipo)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(Detalle)
admin.site.register(Local)

