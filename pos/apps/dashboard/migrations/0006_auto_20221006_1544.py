# Generated by Django 3.2.10 on 2022-10-06 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_userrole_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
