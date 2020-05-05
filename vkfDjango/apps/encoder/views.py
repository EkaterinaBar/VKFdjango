import os
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from pathlib import Path
from .models import FileForEncoder, SampleForVKF
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
        file_path = BASE_DIR + '/'+name
        handle_uploaded_file(request.FILES['fileFOR'], file_path) #сохраняю файл отдельно на сервере, чтобы знать путь к нему
        file_type = Path(file_path).suffix
    except:
         raise Http404("Неправильный путь!")
    if FileForEncoder.objects.filter(file_name=name):
        return render(request, 'encoder/modal.html', {'data': 'Файл с таким именем уже существует в базе. Просмотрите последние файлы.'})
    try:
        f = FileForEncoder(file_name = name, file_path = file_path, file_type = file_type)
        f.save()
    except:
        return render(request, 'encoder/modal.html', {'data': 'Файл не сохранился в базе.'})
    return render(request, 'encoder/modal.html', {'data': 'Файл сохранён в базе'})

def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)