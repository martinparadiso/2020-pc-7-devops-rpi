# Generated by Django 3.1.4 on 2020-12-06 14:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20201206_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='ip',
            field=models.GenericIPAddressField(validators=[django.core.validators.validate_ipv46_address], verbose_name='ip'),
        ),
    ]