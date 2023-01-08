# Generated by Django 3.2.10 on 2022-10-03 18:01

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0005_alter_user_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='PXPermission',
            fields=[
                ('permission_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.permission')),
                ('title', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Permissions',
                'ordering': ['-id'],
            },
            bases=('auth.permission',),
            managers=[
                ('objects', django.contrib.auth.models.PermissionManager()),
            ],
        ),
    ]