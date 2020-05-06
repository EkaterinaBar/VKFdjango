import os
import vkfencoder
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from pathlib import Path
from .models import FileForEncoder, SampleForVKF
from .db_settings import VKFConfig

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #получаю путь до приложения encoder
# Create your views here.
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
    except Exception as e:
        print(e)
        raise Http404("Неправильный путь!")
    if FileForEncoder.objects.filter(file_name=name):
        return render(request, 'encoder/modal.html', {'data': 'Файл с таким именем уже существует в базе. Просмотрите последние файлы.'})
    try:
        f = FileForEncoder(file_name = name, file_path = file_path, file_type = file_type)
        f.save()
    except Exception as e:
        print(e)
        return render(request, 'encoder/modal.html', {'data': 'Файл не сохранился в базе.'})
    return render(request, 'encoder/modal.html', {'data': 'Файл сохранён в базе'})

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
        pathFor = f.file_path #сначала узнаем все нужные пути
        vkfencoder.XMLImport(pathFor, request.POST['tablename_encoder'], request.POST['tablename_orderings'], VKFConfig.DB_NAME, VKFConfig.DB_HOST, VKFConfig.DB_USER, VKFConfig.DB_PSWD)
        f.file_tableEncoder = request.POST['tablename_encoder']
        f.file_tableOrderings = request.POST['tablename_orderings']
        f.save()
    except Exception as e:
        print(e)
        raise Http404("Файл не найден!")
    return render(request, 'encoder/modal.html', {'data': 'Таблицы ' +  request.POST['tablename_encoder'] + ' и ' + request.POST['tablename_orderings'] +' сформированы.','fileForEncoder_id': fileForEncoder_id})