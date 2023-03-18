from django import forms
from .models import *


class TaskForm(forms.Form):

    collection = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    task_name = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=50000, required=False)
    descriptionT = forms.CharField(max_length=50000, required=False)
    cost = forms.DecimalField(max_digits=2, decimal_places=1,widget=forms.TextInput(attrs={'class': 'form-control'}))
    days = forms.IntegerField(max_value=100,widget=forms.TextInput(attrs={'class': 'form-control'}))

