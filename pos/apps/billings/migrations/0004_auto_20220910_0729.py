# Generated by Django 3.2.10 on 2022-09-10 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0003_alter_transaction_reason'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-id'], 'verbose_name_plural': ' Transactions'},
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='outlet',
        ),
    ]
