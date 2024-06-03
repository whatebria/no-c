from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import FormCrearProyecto, ProyectoPatrocinioForm, ProyectoModificarForm
from .models import Proyecto

def plataforma(request):
    data = {
        'login': AuthenticationForm(),
        'Proyectos': Proyecto.objects.all(),
    }

    user = request.user

    # FILTRO
    patrocinio = request.GET.get('filtro')
    if patrocinio == 'con':
        data['Proyectos'] = Proyecto.objects.filter(patrocinio=True)
    elif patrocinio == 'sin':
        data['Proyectos'] = Proyecto.objects.filter(patrocinio=False)
    else:
        data['Proyectos'] = Proyecto.objects.all()
    
    # LOGIN
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            data['mensaje'] = 'Sesión iniciada con éxito'
        else:
            data['mensaje'] = 'Usuario o contraseña incorrecta'

    # PATROCINIO
    patrocinar_form = ProyectoPatrocinioForm(request.POST or None)
    data['patrocinar_form'] = patrocinar_form  # Ensure the form is passed to the template
    if patrocinar_form.is_valid() and user.is_authenticated:
        proyecto = patrocinar_form.save(profesor=user if patrocinar_form.cleaned_data['patrocinar'] else None)
        data['patrocinar'] = proyecto

    # CREACION DE PROYECTO
    if user.is_authenticated and user.groups.filter(name='Estudiante').exists() and request.method == 'POST':
        crear_proyecto_form = FormCrearProyecto(request.POST, user=user)
        if crear_proyecto_form.is_valid():
            crear_proyecto_form.save()
        else:
            data['crearProyecto'] = crear_proyecto_form

     # MODIFICACIÓN DE PROYECTO
    modificar_proyecto_form = ProyectoModificarForm(request.POST or None, instance=None)  # Replace `None` with the instance you want to modify
    data['modificar_proyecto_form'] = modificar_proyecto_form
    if modificar_proyecto_form.is_valid() and user.is_authenticated:
        proyecto_modificado = modificar_proyecto_form
        data['proyecto_modificado'] = proyecto_modificado

    # Render the template with the updated data
    if user.is_authenticated:
        data['crearProyecto'] = FormCrearProyecto(user=user)
    return render(request, 'app/base.html', data)
