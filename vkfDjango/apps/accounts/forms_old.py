from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from vkfsys.models import Experiment
from encoder.models import FileForEncoder, SampleForVKF

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ExperimentForm(ModelForm):
	class Meta:
		model = Experiment
		fields = '__all__'


class FileForm(ModelForm):
	class Meta:
		model = FileForEncoder
		fields = '__all__'