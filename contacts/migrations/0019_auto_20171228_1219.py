# Generated by Django 2.0 on 2017-12-28 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0018_auto_20171228_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='contact_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.ContactPerson'),
        ),
        migrations.AddField(
            model_name='contact',
            name='other_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.OtherDetail'),
        ),
        migrations.AddField(
            model_name='contact',
            name='remarks',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.Remark'),
        ),
    ]
