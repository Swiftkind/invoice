# Generated by Django 2.0 on 2018-01-23 01:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0005_auto_20180122_0600'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('display_name', 'owner')},
        ),
    ]
