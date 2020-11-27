from django.http import HttpResponse
import sensors.temperature
def saludo(request):

    return HttpResponse(sensors.temperature.get_temperature())
