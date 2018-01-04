# Generated by Django 2.0 on 2018-01-03 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0032_auto_20180103_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionaladdress',
            name='fax',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='additionaladdress',
            name='phone',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='additionaladdress',
            name='zip_code',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='fax',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='phone',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='zip_code',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='fax',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='zip_code',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
