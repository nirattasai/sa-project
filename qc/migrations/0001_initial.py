# Generated by Django 3.2.8 on 2021-10-31 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderChecklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.BooleanField(default=False)),
                ('shape', models.BooleanField(default=False)),
                ('jewelry_size', models.BooleanField(default=False)),
                ('product_size', models.BooleanField(default=False)),
                ('overall', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'order_checklists',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('header', 'Header'), ('staff', 'Staff'), ('craftman', 'Craftman')], max_length=20)),
                ('first_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(blank=True, max_length=200, null=True)),
                ('case', models.CharField(blank=True, choices=[('first_time', 'First_time'), ('edit', 'Edit')], max_length=200, null=True)),
                ('status', models.CharField(choices=[("didn't assign", "Didn't assign"), ('waiting', 'Waiting'), ('passed', 'Passed'), ('rejected', 'Rejected'), ('completed', 'Completed')], max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('number', models.CharField(blank=True, max_length=200, null=True)),
                ('shape', models.CharField(blank=True, max_length=200, null=True)),
                ('jewelry_size', models.CharField(blank=True, max_length=200, null=True)),
                ('product_size', models.CharField(blank=True, max_length=200, null=True)),
                ('overall', models.CharField(blank=True, max_length=500, null=True)),
                ('craftman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='craftman', to='qc.profile')),
                ('creater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creater', to=settings.AUTH_USER_MODEL)),
                ('order_checklist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_checklist', to='qc.orderchecklist')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'work_orders',
            },
        ),
        migrations.AddField(
            model_name='orderchecklist',
            name='work_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qc.workorder'),
        ),
        migrations.CreateModel(
            name='MessageOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('sended', 'Sended')], default='waiting', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qc.workorder')),
            ],
            options={
                'db_table': 'message_orders',
            },
        ),
    ]
