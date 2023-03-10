# Generated by Django 3.2.10 on 2022-09-07 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Outlet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('legal_name', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(default='dts@gmail.com', max_length=254)),
                ('status', models.IntegerField(choices=[(1, 'Main'), (2, 'Branch'), (4, 'Inactive'), (8, 'Deleted')], default=2)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.currency')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='outlet_owner', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='outlets.outlet')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='outlet_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Outlets',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OutletMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Owner'), (2, 'Staff'), (4, 'Merchant'), (8, 'Client')], default=2)),
                ('status', models.IntegerField(choices=[(1, 'Inactive'), (2, 'Active'), (4, 'Default'), (8, 'Deleted')], default=1)),
                ('outlet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='outlet_member', to='outlets.outlet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'OutletMembers',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OutletCashBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('currency', models.IntegerField(choices=[(1, 'Uzs'), (2, 'Usd')], default=1)),
                ('status', models.IntegerField(choices=[(1, 'Inactive'), (2, 'Active'), (4, 'Default'), (8, 'Deleted')], default=4)),
                ('outlet', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='outlet_cash', to='outlets.outlet')),
            ],
            options={
                'verbose_name_plural': 'OutletCashBox',
                'ordering': ['id'],
            },
        ),
    ]
