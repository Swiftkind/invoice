# Generated by Django 2.0 on 2018-02-08 05:15

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_auto_20180208_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True),
        ),
    ]