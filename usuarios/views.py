from django.shortcuts import render,redirect
from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json

from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.edit import FormView

from .models import User
from .forms import *
from bases.views import SinPrivilegios

# Create your views here.
class UserListView(SinPrivilegios, generic.ListView):
    model = User
    queryset = User.objects.filter(is_active = True)
    template_name = "usuarios/user_list.html"
    context_object_name = 'obj'
    permission_required="usuarios.view_user"   

class UserRegisterView(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'usuarios/user_form.html'
    success_url= reverse_lazy("usuarios:user_list")
    permission_required='usuarios.add.user'
    context_object_name = 'obj'    

class UserUpdateView(SuccessMessageMixin,SinPrivilegios, generic.UpdateView):
    template_name = "usuarios/user_update.html"    
    model = User    
    permission_required="usuarios.change_user"
    success_url = reverse_lazy("usuarios:user_list")
    
    fields = ['username', 'nombres','apellidos', 'genero', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']        
    labels = {'username': 'Usuario', 'nombres': 'Nombre', 'apellidos': 'Apellidos',
                  'genero': 'Genero','email': 'E-mail','is_active': 'Activo',
                  'is_staff': 'Acceso Administración', 'is_superuser':'Administrador', 'groups':'Asignar Grupo', 'user_permissions':'Asignar Permisos'
             }
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()       
        return super().post(request, *args, **kwargs)    

    def form_valid(self, form):        
        return super(UserUpdateView, self).form_valid(form)
    
class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'usuarios/pass_update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('bases:login')
    login_url = reverse_lazy('bases:login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)   

class UsuarioDel(SuccessMessageMixin, SinPrivilegios, generic.DeleteView):
    model=User
    permission_required="usuarios.delete_user"    
    template_name='usuarios/user_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("usuarios:user_list")
    success_message="Usuario Eliminado Satisfactoriamente"
