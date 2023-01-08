# Generated by Django 3.2.10 on 2022-09-13 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('outlets', '0006_auto_20220910_2144'),
        ('products', '0003_auto_20220913_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inoutproduct',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sell_client', to='outlets.outletcustomer'),
        ),
        migrations.AlterField(
            model_name='inoutproduct',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_provider', to='outlets.outletcustomer'),
        ),
    ]