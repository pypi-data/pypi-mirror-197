# Generated by Django 3.2.7 on 2021-09-21 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sh', '0006_command_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sh_commands', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='savedcommand',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sh_saved_commands', to=settings.AUTH_USER_MODEL),
        ),
    ]
