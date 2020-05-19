from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from vkfsys.models import Experiment
from encoder.models import FileForEncoder, SampleForVKF
from .forms import ExperimentForm

# Create your views here.


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Аккаунт "' + user + '" зарегистрирован')
                return redirect('login')


        context = {'form':form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index")
                
            else:
                messages.info(request, "Неверный логин или пароль")

        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    list_of_exs = Experiment.objects.order_by('id')
    list_of_files = FileForEncoder.objects.order_by('id')
    list_of_samples = SampleForVKF.objects.order_by('id')

    num_exs = list_of_exs.count()
    num_files = list_of_files.count()
    num_samples = list_of_samples.count()

    context = {
        'list_of_exs': list_of_exs,
        'list_of_files': list_of_files,
        'list_of_samples': list_of_samples,
        'num_exs':num_exs,
        'num_files':num_files,
        'num_samples':num_samples,
    }

    return render(request, 'accounts/main.html', context)

@login_required(login_url='login')
def update_ex(request, ex_id):

	ex = Experiment.objects.get(id=ex_id)
	form = ExperimentForm(instance=ex)

	if request.method == 'POST':
		form = ExperimentForm(request.POST, instance=ex)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/update_ex.html', context)

@login_required(login_url='login')
def delete_ex(request, ex_id):
	ex = Experiment.objects.get(id=ex_id)
	if request.method == "POST":
		ex.delete()
		return redirect('/')

	context = {'ex':ex}
	return render(request, 'accounts/delete_ex.html', context)