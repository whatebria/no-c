from django.db import models
from django.conf import settings

class Proyecto(models.Model):
    nombreProyecto = models.CharField(max_length=100, unique=True)
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='proyectos_creados', on_delete=models.CASCADE)
    tema = models.CharField(max_length=100)
    patrocinio = models.BooleanField(default=False)
    profesorPatrocinador = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='proyectos_patrocinados', on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        # Si el proyecto es nuevo, establece el usuario que lo crea como estudiante
        if not self.pk:
            self.estudiante = kwargs.pop('user', None)
        # Si el proyecto ya existe y el campo 'patrocinio' cambió a True, guarda el usuario que realizó el cambio
        elif self.pk is not None and self.patrocinio and 'user' in kwargs:
            self.profesorPatrocinador = kwargs['user']
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombreProyecto

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
