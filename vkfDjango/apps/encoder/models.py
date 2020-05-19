from django.db import models
from django.contrib.auth.models import User

class FileForEncoder(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # привязка к пользователю
    file_name = models.CharField('Название файла', max_length = 100)
    file_path = models.CharField('Путь к файлу', max_length = 200)
    file_type = models.CharField('Тип файла', max_length = 10) #xml или json
    file_tableEncoder = models.CharField('Имя таблицы для кодировщика', max_length = 100)
    file_tableOrderings = models.CharField('Имя таблицы для решеток', max_length = 100)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'Файл для кодировщика'
        verbose_name_plural = 'Файлы для кодировщика'

class SampleForVKF(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # привязка к пользователю
    fileSample_type = models.CharField('Тип файла', max_length = 100) #для обучающей или для тестовой выборки - обуч или тест
    fileSample_name = models.CharField('Название файла', max_length = 100)
    fileSample_path = models.CharField('Путь к файлу', max_length = 200)
    fileSample_attr = models.CharField('Целевое свойство', max_length = 10)
    fileSample_table = models.CharField('Имя таблицы', max_length = 100)
    fileSample_encoder = models.CharField('Имя таблицы-кодировщика', max_length = 100)

    def __str__(self):
        return self.fileSample_name

    class Meta:
        verbose_name = 'Файл для выборки'
        verbose_name_plural = 'Файлы для выборки'