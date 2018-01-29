# Generated by Django 2.0 on 2018-01-26 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180126_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('name', 'company')},
        ),
    ]
