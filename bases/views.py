from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.views import generic

from .models import Idioma,Frase

class MixinFormInvalid:
    def form_invalid(self,form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin, MixinFormInvalid):
    login_url = 'bases:login'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url='bases:login'


class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"

def acceder(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=password)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, F"Bienvenid@ de nuevo {nombre_usuario}")
                return redirect("inv:listado_productos")
            else:
                messages.error(request, "Los datos son incorrectos")
        else:
            messages.error(request, "Los datos son incorrectos")

    form = AuthenticationForm()
    return render(request, "bases/login.html", {"form": form})

def salir(request):
    logout(request)
    messages.success(request, F"Tu sesión se ha cerrado correctamente")
    return redirect("bases:login")

class IdiomaList(generic.ListView):
    template_name = "bases/idiomas.html"
    model = Idioma
    context_object_name="obj"

class FraseList(generic.ListView):
    template_name = "bases/frases.html"
    model = Frase
    context_object_name="obj"

    def get_queryset(self):
        qs = Frase.objects.all()
        idioma_id = self.request.GET.get("lang")
        if idioma_id:
            qs = qs.filter(idioma__id=idioma_id)
        return qs

