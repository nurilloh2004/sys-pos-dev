# Generated by Django 3.2.10 on 2022-09-07 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('outlets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Regions',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='WorkingDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_working_day', models.BooleanField(default=True)),
                ('day', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('work_start', models.TimeField()),
                ('work_end', models.TimeField()),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_day', to='outlets.outlet')),
            ],
            options={
                'verbose_name_plural': 'WorkingDays',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=256)),
                ('status', models.IntegerField(choices=[(1, 'Inactive'), (2, 'Active'), (4, 'Default'), (8, 'Center')], default=2)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='district', to='address.region')),
            ],
            options={
                'verbose_name_plural': 'Districts',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('address1', models.CharField(blank=True, max_length=255)),
                ('address2', models.CharField(blank=True, max_length=255)),
                ('latitude', models.CharField(default='41.123456', max_length=20)),
                ('longitude', models.CharField(default='71.123456', max_length=20)),
                ('type', models.IntegerField(choices=[(1, 'Door'), (2, 'Drop')], default=2)),
                ('status', models.IntegerField(choices=[(1, 'Inactive'), (2, 'Active'), (4, 'Default'), (8, 'Deleted')], default=4)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='district_outlet', to='address.district')),
                ('outlet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shop_address', to='outlets.outlet')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_outlet', to='address.region')),
            ],
            options={
                'verbose_name_plural': 'Addresses',
                'ordering': ['-id'],
            },
        ),
    ]