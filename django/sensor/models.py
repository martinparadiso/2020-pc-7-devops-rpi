from django.db import models
VERSIONES = (
    ("1", "algo"),
    ("2", "algo 2",),)

# Create your models here.
class dispositivo(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre del dispositivo', max_length = 20, null = False)
    ip = models.GenericIPAddressField(null = True)
    Actual = models.CharField('Version Actual', max_length = 20, null = False)
    Update = models.CharField( max_length = 20, choices = VERSIONES, null= True)
 
    class Meta:   
        verbose_name = 'dispositivo'
        verbose_name_plural = 'dispositivos'
    def get_status(self):
        return self.get_status_display()

    get_status.short_description = 'Status'


    def __str__ (self): #como sera reenderizado
    	return self.nombre 
