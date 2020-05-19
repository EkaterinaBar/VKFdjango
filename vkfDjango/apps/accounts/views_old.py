from django.shortcuts import render

# Create your views here.

def loginUser(request):
    pass

def index(request):
    return render(request, 'accounts/main.html')

def logout(request):
    pass