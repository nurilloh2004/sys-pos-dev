# Generated by Django 3.2.10 on 2022-09-10 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billings', '0004_auto_20220910_0729'),
        ('outlets', '0002_auto_20220909_0125'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutletCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Provider'), (2, 'Client')], default=2)),
                ('status', models.IntegerField(choices=[(1, 'Inactive'), (2, 'Active'), (4, 'Default'), (8, 'Deleted')], default=1)),
                ('balance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_balance', to='billings.userbalance')),
                ('outlet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_shop', to='outlets.outlet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': ' OutletCustomers',
                'ordering': ['-id'],
            },
        ),
    ]
