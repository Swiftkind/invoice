# Generated by Django 2.0 on 2018-02-05 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20180205_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_type',
            field=models.CharField(choices=[('fixed', 'Fixed Price'), ('quantity', 'Quantity')], default='fixed', max_length=10),
        ),
    ]
