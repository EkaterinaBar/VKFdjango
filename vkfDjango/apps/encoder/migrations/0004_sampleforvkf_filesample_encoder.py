# Generated by Django 3.0.5 on 2020-05-06 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encoder', '0003_auto_20200506_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleforvkf',
            name='fileSample_encoder',
            field=models.CharField(default='default_encoder', max_length=100, verbose_name='Имя таблицы-кодировщика'),
            preserve_default=False,
        ),
    ]
