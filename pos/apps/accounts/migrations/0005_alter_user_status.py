# Generated by Django 3.2.10 on 2022-09-10 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.IntegerField(choices=[(1, 'Inactive'), (2, 'Active'), (4, 'Deleted')], default=1),
        ),
    ]
