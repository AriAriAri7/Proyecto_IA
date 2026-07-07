from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('diagnostico/', views.iniciar_diagnostico, name='iniciar_diagnostico'),
    path('diagnostico/<int:diagnostico_id>/', views.ver_diagnostico, name='ver_diagnostico'),
    path('resultado/<int:diagnostico_id>/', views.obtener_resultado, name='resultado'),
    path('historial/', views.historial, name='historial'),
    path('manual/', views.manual, name='manual'),
    path('reglas/', views.reglas_lista, name='reglas'),
    path('api/procesar/', views.procesar_respuesta, name='api_procesar'),
    path('api/diagnosticar-rapido/', views.diagnosticar_rapido, name='api_diagnostico_rapido'),
    path('api/preguntas/', views.obtener_preguntas_api, name='api_preguntas'),
    path('api/sintomas/', views.obtener_sintomas_api, name='api_sintomas'),
    path('api/nuevo-diagnostico/', views.nuevo_diagnostico_api, name='api_nuevo_diagnostico'),
]
