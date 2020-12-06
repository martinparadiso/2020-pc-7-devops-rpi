from django.db import models
    

# Create your models here.
class dispositivo(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre del dispositivo', max_length = 20, null = False)
    ip = models.GenericIPAddressField(null = True)

 
    class Meta:   
        verbose_name = 'dispositivo'
        verbose_name_plural = 'dispositivos'


    def __str__ (self): #como sera reenderizado
    	return self.nombre 

   
  
