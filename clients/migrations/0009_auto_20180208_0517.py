# Generated by Django 2.0 on 2018-02-08 05:17

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_auto_20180208_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128),
        ),
    ]
