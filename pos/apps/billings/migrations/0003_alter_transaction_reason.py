# Generated by Django 3.2.10 on 2022-09-08 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0002_auto_20220909_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='reason',
            field=models.IntegerField(choices=[(1, 'Buying'), (2, 'Selling'), (4, 'Credit')], default=1),
        ),
    ]
