# Generated by Django 2.0 on 2018-02-02 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180202_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Company'),
        ),
    ]
