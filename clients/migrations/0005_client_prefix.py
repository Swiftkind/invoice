# Generated by Django 2.0 on 2018-02-08 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20180207_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='prefix',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
