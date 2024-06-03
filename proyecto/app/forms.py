from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Proyecto

class FormCrearProyecto(forms.ModelForm):
    profesores = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Profesor'), required=False, label='Profesor Patrocinador')

    class Meta:
        model = Proyecto
        fields = ('nombreProyecto', 'tema', 'patrocinio', 'profesores')
        labels = {
            'nombreProyecto': 'Nombre Proyecto',
        }
        widgets = {
            'patrocinio': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Guardar el usuario proporcionado desde la vista
        super().__init__(*args, **kwargs)
        # Si el usuario existe y no es un profesor, ocultar los campos 'patrocinio' y 'profesores'
        if self.user and not self.user.groups.filter(name='Profesor').exists():
            self.fields['patrocinio'].widget = forms.HiddenInput()
            self.fields['profesores'].widget = forms.HiddenInput()

    def save(self, commit=True):
        proyecto = super().save(commit=True)
        # Si el usuario está proporcionado, guardar al usuario como el estudiante del proyecto
        if self.user:
            proyecto.estudiante = self.user
        if commit:
            proyecto.save()
        return proyecto


class ProyectoPatrocinioForm(forms.Form):
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), label='Seleccione un proyecto')
    patrocinar = forms.BooleanField(required=False, label='¿Desea patrocinar este proyecto?')

    def save(self, profesor):
        proyecto = self.cleaned_data['proyecto']
        patrocinar = self.cleaned_data['patrocinar']
        if patrocinar:
            proyecto.profesorPatrocinador = profesor
            proyecto.save()
        return proyecto

class ProyectoModificarForm(forms.ModelForm):
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all(), label='Seleccione un proyecto')
    class Meta:
        model = Proyecto
        fields = ['proyecto', 'tema', 'patrocinio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patrocinio'].widget.attrs['disabled'] = 'disabled'

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        # Any additional logic you want to add before saving the instance
        instance.save()
        return instance
