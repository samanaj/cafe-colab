from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
#
from .models import User, Group

class UserRegisterForm(UserCreationForm):
    #para que no se vea la contraseña y pida confirmar contraseña password2
    password1 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeterir Contraseña', required=True, widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        """Meta definition for Userform."""
        model = User
        fields = ['username',  'nombres','apellidos', 'genero', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'u_c','u_m']        
        labels = {'username': 'Username', 'nombres': 'Nombre', 'apellidos': 'Apellido',
                  'genero': 'Genero','email': 'E-mail','is_active': 'Activo',
                  'is_staff': 'Acceso panel', 'is_superuser':'Administrador', 'groups':'Asignar Grupo', 'user_permissions':'Asignar permiso'
                 }
        widgets = {
            'user_permissions': forms.CheckboxSelectMultiple()
        }     
        exclude = ['u_m', 'u_c']

        #validadr password
    def clean_password2(self):
        #recuperamso lo que trae password1 y lo comparo con lo que recuperamos del form en password 2
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            #almomenot de pintar el error nos campuramos el error
                self.add_error('password2', 'Las contraseñas no son iguales')     

    def save(self, commit = True):            
        user = super().save()
        self.save_m2m()
        return user

class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widget={'descripcion': forms.TextInput()}
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
