from django.db import models

class Experiment(models.Model):
    table_enc = models.CharField('Таблица с кодировщиком', max_length = 100) #имя таблицы
    table_samp = models.CharField('Таблица с обучающей выборкой', max_length = 100)  #имя таблицы
    table_hyps = models.CharField('Таблица с гипотезами', max_length = 10)  #имя таблицы
    num_hyps = models.IntegerField('Количество гипотез')
    table_test = models.CharField('Таблица с тестовой выборкой', max_length = 100) #имя таблицы
    num_pos = models.IntegerField('Количество положительных примеров')
    num_neg = models.IntegerField('Количество негативных примеров')

    def __str__(self):
        return self.table_hyps

    class Meta:
        verbose_name = 'ВКФ-эксперимент'
        verbose_name_plural = 'ВКФ-эксперименты'