# Generated by Django 2.0 on 2018-02-02 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('invoices', '0001_initial'),
        ('items', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Company'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='items.Item'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together={('invoice_number', 'company')},
        ),
    ]
