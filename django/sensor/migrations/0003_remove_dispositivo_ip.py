# Generated by Django 3.1.4 on 2020-12-04 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0002_dispositivo_ip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispositivo',
            name='ip',
        ),
    ]
