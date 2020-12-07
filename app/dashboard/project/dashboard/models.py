from django.db import models
from django.core.validators import validate_ipv46_address

class Device(models.Model):
    name = models.CharField('name', max_length=100)
    ip = models.GenericIPAddressField('ip', validators=[validate_ipv46_address])
    date_added = models.DateTimeField('date added')
    last_check = models.DateTimeField('last check', null=True, blank=True)
    last_status = models.CharField('last status', max_length=64, blank=True)
    image = models.CharField('image', max_length=100, blank=True)
    tag = models.CharField('tag', max_length=100, blank=True)
    token = models.CharField('token', max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

    def get_last_check(self):
        if self.last_check is None:
            return "Never"
        else:
            return self.last_check

    def get_last_status(self):
        if self.last_status != "":
            return f"{self.last_status}"
        else:
            return "Unknown"

    def get_image(self):
        if self.image != "":
            return f"{self.image}"
        else:
            return "Unknown"
    
    def get_tag(self):
        if self.tag != "":
            return f"{self.tag}"
        else:
            return "Unknown"

    def get_image_name(self):
        if self.image != "" and self.tag != "":
            return f"{self.image}:{self.tag}"
        else:
            return "Unknown"
