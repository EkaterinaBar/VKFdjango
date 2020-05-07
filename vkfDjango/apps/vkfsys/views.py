import os
import vkf
import pymysql
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from pathlib import Path
from .models import Experiment
from .db_settings import VKFConfig
from encoder.models import FileForEncoder, SampleForVKF

def index(request):
    return render(request, 'vkfsys/main.html')

def induction(request):
    filesFor = FileForEncoder.objects.order_by('file_name')
    trainSamples = SampleForVKF.objects.order_by('fileSample_name')
    list_of_samples = []
    dict_of_filesFor = {} #создаю словарь с таблицами encoder и обучающими выборками для них
    if filesFor:
        for f in filesFor: 
            list_of_samples = []
            if trainSamples:
                for s in trainSamples:
                    if s.fileSample_encoder == f.file_tableEncoder and s.fileSample_type == 'train':
                        list_of_samples.append(s)
            dict_of_filesFor[f]=list_of_samples
    return render(request, 'vkfsys/induction.html', {'dict_of_filesFor':dict_of_filesFor})

def create_table(request):
    url = '/vkfsys/induction'
    try:
        table_enc = request.POST['table_enc']
        table_samp = request.POST['table_samp']
    except Exception as e:
        print(e)
        return render(request, 'encoder/modal.html', {'data': 'Вы не выбрали таблицы', 'urlForAction': url})
    table_hyps = request.POST['table_hyps']
    num_hyps = request.POST['num_hyps']
    num_thr = request.POST['num_thr']
    if table_hyps == '' or num_hyps == '' or num_thr == '':
        return render(request, 'vkfsys/modal.html', {'data': 'Вы ввели неправильные данные или не ввели данные', 'urlForAction': url}) 
    try:
        con = pymysql.connect(VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD, VKFConfig.DB_NAME) 
        with con: 
            cur = con.cursor()
            cur.execute("DROP TABLE " + table_hyps + ';')
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе удаления существующей таблицы из базы: '+ str(e), 'urlForAction': url}) 

    try:
        enc = vkf.Encoder(table_enc, VKFConfig.DB_NAME, VKFConfig.DB_HOST,VKFConfig.DB_USER, VKFConfig.DB_PSWD)
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе vkf.Encoder: '+ str(e), 'urlForAction': url}) 
    try:
        ind = vkf.Induction()
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе vkf.Induction: '+ str(e), 'urlForAction': url}) 
    try:  
        ind.load_hypotheses(enc, table_samp, table_hyps, VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе vkf.load_hypotheses: '+ str(e), 'urlForAction': url}) 
    try: 
        ind.add_hypotheses(int(num_hyps), int(num_thr))
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе vkf.add_hypotheses: '+ str(e), 'urlForAction': url}) 
    try: 
        ind.save_hypotheses(enc, table_hyps, VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе vkf.save_hypotheses: '+ str(e), 'urlForAction': url})

    try:
        ex = Experiment(table_enc = table_enc, table_samp = table_samp, table_hyps = table_hyps, num_hyps = num_hyps, table_test = '', num_pos = 0, num_neg = 0)
        ex.save()
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе записи информации об эксперименте в базу: '+ str(e), 'urlForAction': url})

    return render(request, 'vkfsys/create_table.html', {'data': ' Таблица с гипотезами '+ table_hyps + ' создана', 'ex': ex}) 