# Generated by Django 3.2.10 on 2022-10-04 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_selectedpermission_userrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='name',
            field=models.CharField(default='test-1', max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userrole',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to=settings.AUTH_USER_MODEL),
        ),
    ]