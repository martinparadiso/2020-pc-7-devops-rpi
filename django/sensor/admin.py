from django.shortcuts import render
from django.contrib import admin
from .models import *
import VersionDispositivo.version_disp
import requests

class dispositivoAdmin(admin.ModelAdmin):
	search_fields = ['nombre']  #barra de busqueda
	list_display = ('nombre', 'ip','view_version_disp')  #lista 
	
	def view_version_disp(self, obj):
		url=f'http://{obj.ip}:1221/version'
		resultado=requests.get(url)
		resultado=resultado.json()['version']
		return resultado


# Register your models here.



admin.site.register(dispositivo,dispositivoAdmin) #vincula DispositivoAdmin con el registro.
						  #es necesario para la barra de busq
