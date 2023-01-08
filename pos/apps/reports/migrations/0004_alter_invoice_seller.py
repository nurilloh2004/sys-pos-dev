# Generated by Django 3.2.10 on 2022-09-10 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0004_auto_20220910_0729'),
        ('reports', '0003_auto_20220909_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seller_bln', to='billings.billingaccount'),
        ),
    ]
