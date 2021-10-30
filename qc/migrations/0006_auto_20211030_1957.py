# Generated by Django 3.2.8 on 2021-10-30 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qc', '0005_auto_20211030_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[("didn't assign", "Didn't assign"), ('waiting', 'Waiting'), ('completed', 'Completed'), ('rejected', 'Rejected')], max_length=200),
        ),
    ]
