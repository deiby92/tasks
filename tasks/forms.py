from django import forms
from .models import tarea, Profile
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = tarea
        fields = ['Titulo', 'descripcion', 'importante']
        widgets = {
            'Titulo':forms.TextInput(attrs={'class':'form-control', 'placeholder':'escribir titulo'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control', 'placeholder':'ingresar descripcion'}),
            'importante':forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        
class UserForm(forms.ModelForm):
    class Meta: 
        model = User
        fields =['first_name', 'last_name']

class update(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['direccion','telefono']

class ResetPasswordForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Ingrese correo', 'class':'form-control', 'autocomplete':'off'}))