# Generated by Django 2.0 on 2017-12-28 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='other_detail',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contacts.OtherDetail'),
        ),
    ]
