# Generated by Django 2.0 on 2018-02-05 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20180205_0713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.PositiveIntegerField(),
        ),
    ]