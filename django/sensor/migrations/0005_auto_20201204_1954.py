# Generated by Django 3.1.4 on 2020-12-04 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensor', '0004_dispositivo_ip'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dispositivo',
            options={'verbose_name': 'dispositivo', 'verbose_name_plural': 'dispositivos'},
        ),
    ]
