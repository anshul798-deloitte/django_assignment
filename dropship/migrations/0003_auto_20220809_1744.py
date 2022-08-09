# Generated by Django 2.2.4 on 2022-08-09 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dropship', '0002_auto_20220809_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to=settings.AUTH_USER_MODEL),
        ),
    ]
