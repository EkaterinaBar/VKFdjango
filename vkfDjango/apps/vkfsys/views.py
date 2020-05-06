import os
import vkf
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from pathlib import Path
from .models import Experiment
from .db_settings import VKFConfig

def index(request):
    return render(request, 'vkfsys/main.html')
