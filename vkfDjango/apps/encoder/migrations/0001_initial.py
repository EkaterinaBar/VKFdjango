# Generated by Django 3.0.5 on 2020-05-05 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileForEncoder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100, verbose_name='Название файла')),
                ('file_path', models.CharField(max_length=200, verbose_name='Путь к файлу')),
                ('file_type', models.CharField(max_length=10, verbose_name='Тип файла')),
                ('file_tableEncoder', models.CharField(max_length=100, verbose_name='Имя таблицы для кодировщика')),
                ('file_tableOrderings', models.CharField(max_length=100, verbose_name='Имя таблицы для решеток')),
            ],
            options={
                'verbose_name': 'Файл для кодировщика',
                'verbose_name_plural': 'Файлы для кодировщика',
            },
        ),
        migrations.CreateModel(
            name='TrainSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileTRAIN_type', models.CharField(max_length=100, verbose_name='Тип файла')),
                ('fileTRAIN_name', models.CharField(max_length=100, verbose_name='Название файла')),
                ('fileTRAIN_path', models.CharField(max_length=200, verbose_name='Путь к файлу')),
                ('fileTRAIN_attr', models.CharField(max_length=10, verbose_name='Целевое свойство')),
                ('fileTRAIN_table', models.CharField(max_length=100, verbose_name='Имя таблицы')),
            ],
            options={
                'verbose_name': 'Файл для выборки',
                'verbose_name_plural': 'Файлы для выборки',
            },
        ),
    ]
