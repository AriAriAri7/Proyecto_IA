from django.contrib import admin
from .models import Diagnostico, Regla, SesionDiagnostico


@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'falla_encontrada', 'estado', 'confianza', 'fecha_inicio']
    list_filter = ['estado', 'falla_encontrada', 'fecha_inicio']
    search_fields = ['diagnostico_final', 'falla_encontrada', 'usuario__username']
    readonly_fields = ['fecha_inicio', 'fecha_fin', 'tiempo_respuesta']


@admin.register(Regla)
class ReglaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'categoria', 'conclusion', 'prioridad', 'activa']
    list_filter = ['categoria', 'activa']
    search_fields = ['nombre', 'codigo', 'conclusion']


@admin.register(SesionDiagnostico)
class SesionDiagnosticoAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'activa', 'fecha_creacion', 'fecha_actualizacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['session_key']
