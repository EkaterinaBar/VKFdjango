import os
import vkfencoder
import pymysql
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from pathlib import Path
from .models import FileForEncoder, SampleForVKF
from .db_settings import VKFConfig
from django.contrib.auth.decorators import login_required

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #получаю путь до приложения encoder

@login_required(login_url='login')
def index(request):
    #return HttpResponse("hello")
    return render(request, 'encoder/main.html')

def choiceFileFor(request):
    return render(request, 'encoder/choiceFileFor.html')

def add_fileFOR(request):
    try:
        name = request.FILES['fileFOR'].name
        file_path = BASE_DIR + '/files/'+name
        handle_uploaded_file(request.FILES['fileFOR'], file_path) #сохраняю файл отдельно на сервере, чтобы знать путь к нему
        file_type = Path(file_path).suffix
        url = '/encoder/choiceFileFor' #путь для возвращения из модальной формы
    except Exception as e:
        print(e)
        raise Http404("Неправильный путь!")
    if FileForEncoder.objects.filter(file_name=name):
        return render(request, 'vkfsys/modal.html', {'data': 'Файл с таким именем уже существует в базе. Просмотрите загруженные файлы.', 'urlForAction': url})
    try:
        f = FileForEncoder(file_name=name, file_path=file_path, file_type=file_type, user=request.user)
        f.save()
    except Exception as e:
        print(e)
        return render(request, 'vkfsys/modal.html', {'data': 'Файл не сохранился в базе.','urlForAction': url}) 
    return render(request, 'vkfsys/modal.html', {'data': 'Файл сохранён в базе','urlForAction': url})

def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def list_filesFor(request):
    filesFor = FileForEncoder.objects.order_by('file_name')
    return render(request, 'encoder/list_filesFor.html', {'filesFor': filesFor})

def fileFrom(request, fileForEncoder_id):
    try:
        f = FileForEncoder.objects.get(id = fileForEncoder_id)
    except:
        raise Http404("Файл не найден!")
    return render(request, 'encoder/fileFrom.html', {'fileFor': f})

def fill_names(request, fileForEncoder_id):
    try:
        f = FileForEncoder.objects.get(id = fileForEncoder_id)
    except:
        raise Http404("Файл не найден!")
    return render(request, 'encoder/fill_names.html', {'fileFor': f})

def execute(request, fileForEncoder_id):
    try:
        f = FileForEncoder.objects.get(id = fileForEncoder_id)
        pathFor = f.file_path #сначала узнаем путь из бд
        url = '/encoder/fileFrom/'+str(f.id) #путь для возвращения из модальной формы
        if f.file_type == '.xml':
            vkfencoder.XMLImport(pathFor, request.POST['tablename_encoder'], request.POST['tablename_orderings'], VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
        elif f.file_type == '.json':
            vkfencoder.JSONImport(pathFor, request.POST['tablename_encoder'], request.POST['tablename_orderings'], VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
        else:
            raise Http404("Неверное расширение файла!")
        f.file_tableEncoder = request.POST['tablename_encoder']
        f.file_tableOrderings = request.POST['tablename_orderings']
        f.save()
    except Exception as e:
        print(e)
        raise Http404("Файл не найден!")
    return render(request, 'vkfsys/modal.html', {'data': 'Таблицы ' +  request.POST['tablename_encoder'] + ' и ' + request.POST['tablename_orderings'] +' сформированы.','fileForEncoder_id': fileForEncoder_id, 'urlForAction': url})

def show_table(request,fileForEncoder_id,table_name, table_type):
    try:
        if table_type == 'files':
            f = FileForEncoder.objects.get(id = fileForEncoder_id)
            url ='/encoder/fileFrom/' + str(f.id) 
        elif table_type == 'samples':
            f = SampleForVKF.objects.get(id = fileForEncoder_id)
            url = "/encoder/create_table/list_samples"
        else:
            raise Http404("Неизвестный тип!")
        con = pymysql.connect(VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD, VKFConfig.DB_NAME) 
        with con: 
            cur = con.cursor()
            cur.execute("SELECT * FROM " + table_name)
            rows = cur.fetchall()
            cur.execute("SHOW columns FROM " + table_name)  # получаю информацию о именах колонок
            names = cur.fetchall()
        lst_names = []
        for row in names:  # вытаскиваю имена колонок
            lst_names.append(row[0])
    except Exception as e:
        print(e)
        raise Http404("Файл не найден!")
    return render(request, 'encoder/show_table.html', {'rows': rows,'fileFor': f, 'table_name': table_name, 'urlForAction': url, 'names': lst_names})

def create_file(request,fileForEncoder_id, file_type): 
    try: 
        f = FileForEncoder.objects.get(id = fileForEncoder_id)
        pathFor = f.file_path #сначала узнаем путь из бд
        name = Path(pathFor).stem #берем имя без расширения
        url = '/encoder/fileFrom/'+str(f.id)
        if file_type == 'xml':
            pathFor = BASE_DIR + '/files/'+ name + '.xml'
            vkfencoder.XMLExport(pathFor, f.file_tableEncoder, f.file_tableOrderings, VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
        elif file_type == 'json':
            pathFor = BASE_DIR + '/files/'+ name + '.json'
            vkfencoder.JSONExport(pathFor, f.file_tableEncoder, f.file_tableOrderings, VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
        else:
            raise Http404("Неверное расширение файла!")
    except Exception as e:
        print(e)
        raise Http404("Файл не найден!")
    return render(request, 'vkfsys/modal.html', {'data': 'Файл сформирован. Его можно найти в: ' + pathFor, 'urlForAction': url})

def create_table(request):
    filesFor = FileForEncoder.objects.order_by('file_name')
    return render(request, 'encoder/create_table.html', {'filesFor': filesFor})

def add_sample(request):
    url = '/encoder/create_table'
    try:
        name = request.FILES['sample_file'].name
        file_path = BASE_DIR + '/files/'+name
        handle_uploaded_file(request.FILES['sample_file'], file_path) #сохраняю файл отдельно на сервере, чтобы знать путь к нему
        fileSample_type = request.POST['sample_type']
        fileSample_attr = request.POST['sample_attr']
        fileSample_table = request.POST['sample_table']
        fileSample_encoder = request.POST['sample_encoder']
    except Exception as e:
        print(e)
        return render(request, 'vkfsys/modal.html', {'data': 'Выборка не сохранилась в базе. Ошибка: '+ str(e), 'urlForAction': url})
    if SampleForVKF.objects.filter(fileSample_name=name, fileSample_encoder=fileSample_encoder, fileSample_attr=fileSample_attr):
        return render(request, 'vkfsys/modal.html', {'data': 'Таблица для файла с таким именем, кодировщиком и целевым свойством уже существует в базе. Просмотрите существующие выборки.', 'urlForAction': url})
    try:
        vkfencoder.DataImport(file_path, fileSample_attr, fileSample_encoder, fileSample_table, VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
        f = SampleForVKF(user=request.user, fileSample_type = fileSample_type, fileSample_name = name, fileSample_path = file_path, fileSample_attr = fileSample_attr, fileSample_table = fileSample_table, fileSample_encoder = fileSample_encoder)
        f.save()
    except Exception as e:
        print(e)
        return render(request, 'vkfsys/modal.html', {'data': 'Выборка не сохранилась в базе. Ошибка: '+ str(e), 'urlForAction': url})
    return render(request, 'vkfsys/modal.html', {'data': 'Выборка сохранилась в базе', 'urlForAction': url})


def list_samples(request):
    samples = SampleForVKF.objects.order_by('fileSample_name')
    return render(request, 'encoder/list_samples.html', {'samples': samples})