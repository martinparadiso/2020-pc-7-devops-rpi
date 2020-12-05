from django.contrib import admin
from .models import *

class dispositivoAdmin(admin.ModelAdmin):
	search_fields = ['nombre']  #barra de busqueda
	list_display = ('nombre', 'ip','get_status',)  #lista por nombre e ip




# Register your models here.



admin.site.register(dispositivo,dispositivoAdmin) #vincula DispositivoAdmin con el registro.
						  #es necesario para la barra de busq
