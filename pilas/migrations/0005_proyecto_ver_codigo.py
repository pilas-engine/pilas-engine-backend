# Generated by Django 2.0.6 on 2019-07-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pilas', '0004_proyecto_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='ver_codigo',
            field=models.BooleanField(default=True),
        ),
    ]
