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

enc = None
ind = None

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
        return render(request, 'vkfsys/modal.html', {'data': 'Вы не выбрали таблицы', 'urlForAction': url})
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
        global enc
        enc = vkf.Encoder(table_enc, VKFConfig.DB_NAME, VKFConfig.DB_HOST,VKFConfig.DB_USER, VKFConfig.DB_PSWD)
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе vkf.Encoder: '+ str(e), 'urlForAction': url}) 
    try:
        global ind
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

def show_table(request, ex_id):
    url = '/vkfsys/induction/create_table/ct_return/'+ str(ex_id)
    try:
        ex = Experiment.objects.get(id = ex_id) 
    except Exception as e:
        raise Http404("Файл не найден: "+ str(e))
    try:
        dict_of_hyps = {}
        global ind, enc
        for i in range(ex.num_hyps):
            list_of_attr_one_hyp =  ind.show_hypothesis(enc, i) #i - номер гипотезы.
            dict_of_hyps[i] = list_of_attr_one_hyp
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе создания списка гипотез с признаками: '+ str(e), 'urlForAction': url})

    table_name = ex.table_hyps 
    # try:
    #     con = pymysql.connect(VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD, VKFConfig.DB_NAME) 
    #     with con: 
    #         cur = con.cursor()
    #         cur.execute("SELECT * FROM " + table_name)
    #         rows = cur.fetchall()
    # except Exception as e:
    #     raise Http404("Ошибка при чтении данных из таблицы: " + str(e))

    return render(request, 'vkfsys/show_table.html', {'dict_of_hyps': dict_of_hyps,'ex': ex, 'table_name': table_name})

def ct_return(request, ex_id):
    try:
        ex = Experiment.objects.get(id = ex_id) 
    except Exception as e:
        raise Http404("Файл не найден: "+ str(e))
    return render(request, 'vkfsys/create_table.html', {'data': 'Таблица с гипотезами ' + ex.table_hyps, 'ex': ex}) 

def for_add_hyps(request, ex_id):
    return render(request, 'vkfsys/for_add_hyps.html', {'ex_id': ex_id}) 

def add_hyps(request, ex_id):
    try:
        ex = Experiment.objects.get(id = ex_id) 
    except Exception as e:
        raise Http404("Файл не найден: "+ str(e))
    table_enc = ex.table_enc
    table_samp = ex.table_samp
    table_hyps = ex.table_hyps
    num_hyps = request.POST['num_hyps']
    num_thr = request.POST['num_thr']
    url = '/vkfsys/induction/create_table/ct_return/' + str(ex_id)
    if num_hyps=='' or num_thr=='':
        return render(request, 'vkfsys/modal.html', {'data': 'Вы ввели неправильные данные или не ввели данные', 'urlForAction': url})     
    try: 
        global ind
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
        ex.num_hyps += int(num_hyps)
        ex.save()
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе сохранения нового значения количества гипотез: '+ str(e), 'urlForAction': url})
    
    return render(request, 'vkfsys/create_table.html', {'data': 'Гипотезы добавлены. В количестве: ' + num_hyps, 'ex': ex}) 

def choice_test(request, ex_id):
    try:
        ex = Experiment.objects.get(id = ex_id) 
    except Exception as e:
        raise Http404("Файл не найден: "+ str(e))
    samples = SampleForVKF.objects.order_by('fileSample_name')
    test_samples = [] #список тестовых выборок для нашего table_enc 
    if samples:
        for s in samples:
            if s.fileSample_encoder == ex.table_enc and s.fileSample_type == 'test':
                test_samples.append(s)
    return render(request, 'vkfsys/choice_test.html', {'test_samples':test_samples, 'ex_id':ex_id})

def prediction(request, ex_id):
    try:
        ex = Experiment.objects.get(id = ex_id) 
    except Exception as e:
        raise Http404("Файл не найден: "+ str(e))
    table_enc = ex.table_enc
    table_samp = ex.table_samp
    table_hyps = ex.table_hyps
    url = '/vkfsys/induction/create_table/choice_test/' + str(ex_id)
    try:
        table_test = request.POST['table_test']
    except Exception as e:
        print(e)
        return render(request, 'vkfsys/modal.html', {'data': 'Вы не выбрали таблицу с выборкой', 'urlForAction': url})
    
    try:
        global ind
        ind.load_hypotheses(enc, table_samp, table_hyps, VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе vkf.load_hypotheses: '+ str(e), 'urlForAction': url}) 
    try:    
        tes = vkf.TestSample(enc, ind, table_test, VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе vkf.TestSample: '+ str(e), 'urlForAction': url}) 
   
    positive=str(tes.correct_positive_cases())
    negative=str(tes.correct_negative_cases())

    try:
        ex.table_test = table_test
        ex.num_pos = positive
        ex.num_neg = negative
        ex.save()
    except Exception as e:
        return render(request, 'vkfsys/modal.html', {'data': 'Ошибка на этапе сохранения результатов в базу: '+ str(e), 'urlForAction': url}) 
    return render(request, 'vkfsys/results.html', {'positive': positive, 'negative': negative}) 

def list_exs(request):
    list_of_exs = Experiment.objects.order_by('id')
    return render(request, 'vkfsys/list_of_exs.html', {'list_of_exs': list_of_exs})