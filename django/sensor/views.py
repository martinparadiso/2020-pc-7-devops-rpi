from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import versiones.rel
def version(request):

    return HttpResponse(versiones.rel.get_version())
