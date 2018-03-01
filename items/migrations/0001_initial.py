# Generated by Django 2.0 on 2018-02-02 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoiced', models.BooleanField(default=False)),
                ('item_type', models.CharField(choices=[('fixed', 'Fixed Price'), ('hourly', 'Hourly')], default='fixed', max_length=10)),
                ('order_number', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('rate', models.PositiveIntegerField(blank=True, null=True)),
                ('hours', models.PositiveIntegerField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('amount', models.PositiveIntegerField(blank=True, null=True)),
                ('total_amount', models.PositiveIntegerField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]