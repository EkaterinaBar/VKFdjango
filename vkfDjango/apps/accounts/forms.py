from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from vkfsys.models import Experiment

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ExperimentForm(ModelForm):
	class Meta:
		model = Experiment
		fields = '__all__'