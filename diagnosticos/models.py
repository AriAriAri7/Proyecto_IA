from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Diagnostico(models.Model):
    ESTADOS = [
        ('en_curso', 'En curso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuario')
    sesion_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID de sesion')
    fecha_inicio = models.DateTimeField(default=timezone.now, verbose_name='Fecha de inicio')
    fecha_fin = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalizacion')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_curso', verbose_name='Estado')
    sintomas = models.JSONField(default=dict, blank=True, verbose_name='Sintomas reportados')
    diagnostico_final = models.TextField(blank=True, null=True, verbose_name='Diagnostico final')
    falla_encontrada = models.CharField(max_length=100, blank=True, null=True, verbose_name='Falla encontrada')
    recomendaciones = models.JSONField(default=list, blank=True, verbose_name='Recomendaciones')
    reglas_aplicadas = models.JSONField(default=list, blank=True, verbose_name='Reglas aplicadas')
    confianza = models.IntegerField(default=0, verbose_name='Nivel de confianza (%)')
    tiempo_respuesta = models.FloatField(default=0, verbose_name='Tiempo de respuesta (segundos)')
    ip_usuario = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP del usuario')

    class Meta:
        verbose_name = 'Diagnostico'
        verbose_name_plural = 'Diagnosticos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Diagnostico #{self.id} - {self.get_estado_display()} - {self.fecha_inicio.strftime('%d/%m/%Y %H:%M')}"

    def duracion(self):
        if self.fecha_fin and self.fecha_inicio:
            delta = self.fecha_fin - self.fecha_inicio
            return f"{delta.seconds // 60} min {delta.seconds % 60} seg"
        return 'En curso'


class Regla(models.Model):
    CATEGORIAS = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('red', 'Red'),
    ]

    nombre = models.CharField(max_length=200, verbose_name='Nombre de la regla')
    codigo = models.CharField(max_length=10, unique=True, verbose_name='Codigo')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, verbose_name='Categoria')
    condiciones = models.JSONField(default=dict, verbose_name='Condiciones (JSON)')
    conclusion = models.CharField(max_length=100, verbose_name='Conclusion')
    acciones = models.JSONField(default=list, verbose_name='Acciones recomendadas')
    explicacion = models.TextField(blank=True, verbose_name='Explicacion')
    prioridad = models.IntegerField(default=10, verbose_name='Prioridad (menor = mayor prioridad)')
    activa = models.BooleanField(default=True, verbose_name='Activa')

    class Meta:
        verbose_name = 'Regla'
        verbose_name_plural = 'Reglas'
        ordering = ['prioridad']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class SesionDiagnostico(models.Model):
    session_key = models.CharField(max_length=100, unique=True, verbose_name='Clave de sesion')
    datos = models.JSONField(default=dict, blank=True, verbose_name='Datos de la sesion')
    reglas_aplicadas = models.JSONField(default=list, blank=True, verbose_name='Reglas aplicadas')
    preguntas_realizadas = models.JSONField(default=list, blank=True, verbose_name='Preguntas realizadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Ultima actualizacion')
    activa = models.BooleanField(default=True, verbose_name='Activa')

    class Meta:
        verbose_name = 'Sesion de diagnostico'
        verbose_name_plural = 'Sesiones de diagnostico'

    def __str__(self):
        return f"Sesion {self.session_key[:20]}... - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
