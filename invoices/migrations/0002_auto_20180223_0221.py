# Generated by Django 2.0 on 2018-02-23 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_company_owner'),
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together={('company', 'invoice_number')},
        ),
    ]
