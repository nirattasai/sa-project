# Generated by Django 3.2.8 on 2021-11-05 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_joined',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
