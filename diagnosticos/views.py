import json
import logging
import time
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count

from .models import Diagnostico, Regla, SesionDiagnostico
from conocimiento.motor_inferencia import FallasKnowledgeEngine
from conocimiento.base_conocimiento import BaseConocimiento
from conocimiento.preguntas import PreguntasManager

logger = logging.getLogger('diagnosticos')
motor = FallasKnowledgeEngine()
base_cono = BaseConocimiento()
preguntas_mgr = PreguntasManager()


def index(request):
    context = {
        'total_diagnosticos': Diagnostico.objects.count(),
        'diagnosticos_completados': Diagnostico.objects.filter(estado='completado').count(),
        'total_reglas': Regla.objects.filter(activa=True).count(),
        'fallas_comunes': Diagnostico.objects.filter(estado='completado').values('falla_encontrada').annotate(
            total=Count('falla_encontrada')).order_by('-total')[:5],
        'ultimos_diagnosticos': Diagnostico.objects.filter(estado='completado').order_by('-fecha_fin')[:5],
    }
    return render(request, 'diagnosticos/index.html', context)


def iniciar_diagnostico(request):
    sintomas = base_cono.obtener_todos_sintomas()

    if request.method == 'POST':
        sintoma_id = request.POST.get('sintoma_principal', '')
        if not sintoma_id:
            messages.warning(request, 'Por favor selecciona un sintoma principal.')
            return render(request, 'diagnosticos/diagnostico.html', {'sintomas': sintomas})

        diagnostico = Diagnostico.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            sesion_id=request.session.session_key or '',
            estado='en_curso',
            sintomas={'sintoma_principal': sintoma_id},
        )

        preguntas = motor.generar_preguntas(sintoma_id)
        request.session['diagnostico_activo'] = diagnostico.id
        request.session['preguntas_diagnostico'] = [p['id'] for p in preguntas]
        request.session['pregunta_actual_idx'] = 0

        return redirect('ver_diagnostico', diagnostico_id=diagnostico.id)

    ultimo_diagnostico = None
    diag_id = request.session.get('diagnostico_activo')
    if diag_id:
        try:
            ultimo_diagnostico = Diagnostico.objects.get(id=diag_id)
        except Diagnostico.DoesNotExist:
            pass

    context = {
        'sintomas': sintomas,
        'ultimo_diagnostico': ultimo_diagnostico,
    }
    return render(request, 'diagnosticos/diagnostico.html', context)


def ver_diagnostico(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
    preguntas_ids = request.session.get('preguntas_diagnostico', [])
    idx = request.session.get('pregunta_actual_idx', 0)

    pregunta_actual = None
    if idx < len(preguntas_ids):
        pregunta_actual = preguntas_mgr.obtener_pregunta(preguntas_ids[idx])

    progreso = int((idx / len(preguntas_ids)) * 100) if preguntas_ids else 0

    context = {
        'diagnostico': diagnostico,
        'pregunta_actual': pregunta_actual,
        'progreso': progreso,
        'total_preguntas': len(preguntas_ids),
        'pregunta_numero': idx + 1,
    }
    return render(request, 'diagnosticos/diagnostico.html', context)


def obtener_resultado(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
    falla = base_cono.obtener_falla(diagnostico.falla_encontrada) if diagnostico.falla_encontrada else None

    context = {
        'diagnostico': diagnostico,
        'falla': falla,
        'recomendaciones': diagnostico.recomendaciones or [],
        'reglas_detalle': diagnostico.reglas_aplicadas or [],
    }
    return render(request, 'diagnosticos/resultado.html', context)


def historial(request):
    diagnosticos = Diagnostico.objects.all().order_by('-fecha_inicio')
    fallas_count = Diagnostico.objects.filter(estado='completado').values('falla_encontrada').annotate(
        total=Count('falla_encontrada')).order_by('-total')

    context = {
        'diagnosticos': diagnosticos,
        'fallas_count': fallas_count,
        'total': diagnosticos.count(),
    }
    return render(request, 'diagnosticos/historial.html', context)


def manual(request):
    context = {
        'total_reglas': len(motor.reglas_manager.obtener_todas()),
        'total_preguntas': len(preguntas_mgr.obtener_todas()),
        'categorias': ['hardware', 'software', 'red', 'mantenimiento', 'rendimiento'],
    }
    return render(request, 'diagnosticos/manual.html', context)


def reglas_lista(request):
    reglas = motor.reglas_manager.obtener_todas()
    categoria = request.GET.get('categoria', '')
    if categoria:
        reglas = [r for r in reglas if r['categoria'] == categoria]

    categorias = list(set(r['categoria'] for r in reglas))
    context = {
        'reglas': reglas,
        'categorias': categorias,
        'categoria_seleccionada': categoria,
    }
    return render(request, 'diagnosticos/reglas.html', context)


@require_POST
def procesar_respuesta(request):
    try:
        data = json.loads(request.body)
        pregunta_id = data.get('pregunta_id', '')
        respuesta = data.get('respuesta', '')
        diagnostico_id = data.get('diagnostico_id') or request.session.get('diagnostico_activo')

        if not diagnostico_id:
            return JsonResponse({'error': 'No hay diagnostico activo'}, status=400)

        diagnostico = Diagnostico.objects.get(id=diagnostico_id)
        pregunta = preguntas_mgr.obtener_pregunta(pregunta_id)

        if not pregunta:
            return JsonResponse({'error': 'Pregunta no encontrada'}, status=404)

        variable = pregunta['variable']
        valor = respuesta

        if isinstance(respuesta, str):
            if respuesta.lower() == 'true':
                valor = True
            elif respuesta.lower() == 'false':
                valor = False

        sintomas = diagnostico.sintomas or {}
        sintomas[variable] = valor
        diagnostico.sintomas = sintomas
        diagnostico.save()

        motor.agregar_hecho(variable, valor)

        preguntas_ids = request.session.get('preguntas_diagnostico', [])
        idx = request.session.get('pregunta_actual_idx', 0)
        idx += 1
        request.session['pregunta_actual_idx'] = idx

        completo = idx >= len(preguntas_ids)
        siguiente_pregunta = None

        if not completo and idx < len(preguntas_ids):
            siguiente_pregunta = preguntas_mgr.obtener_pregunta(preguntas_ids[idx])

        if completo or not siguiente_pregunta:
            resultado = motor.inferir(dict(sintomas))

            diagnostico.estado = 'completado'
            diagnostico.fecha_fin = timezone.now()
            diagnostico.diagnostico_final = resultado['nombre_falla']
            diagnostico.falla_encontrada = resultado['falla_encontrada']
            diagnostico.recomendaciones = resultado['recomendaciones']
            diagnostico.reglas_aplicadas = resultado.get('reglas_detalle', [])
            diagnostico.confianza = resultado['confianza']
            diagnostico.save()

            request.session.pop('diagnostico_activo', None)
            request.session.pop('preguntas_diagnostico', None)
            request.session.pop('pregunta_actual_idx', None)

            return JsonResponse({
                'completo': True,
                'resultado': resultado,
                'diagnostico_id': diagnostico.id,
                'redirect_url': f'/resultado/{diagnostico.id}/'
            })

        progreso = int((idx / len(preguntas_ids)) * 100)

        return JsonResponse({
            'completo': False,
            'pregunta': siguiente_pregunta,
            'progreso': progreso,
            'pregunta_numero': idx + 1,
            'total_preguntas': len(preguntas_ids),
        })

    except Diagnostico.DoesNotExist:
        return JsonResponse({'error': 'Diagnostico no encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Error en procesar_respuesta: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
def diagnosticar_rapido(request):
    try:
        data = json.loads(request.body)
        sintomas = data.get('sintomas', {})

        if not sintomas:
            return JsonResponse({'error': 'Debes proporcionar al menos un sintoma'}, status=400)

        diagnostico = Diagnostico.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            sesion_id=request.session.session_key or '',
            estado='en_curso',
            sintomas=sintomas,
        )

        inicio = time.time()
        resultado = motor.inferir(sintomas)
        tiempo_respuesta = time.time() - inicio

        diagnostico.estado = 'completado'
        diagnostico.fecha_fin = timezone.now()
        diagnostico.diagnostico_final = resultado['nombre_falla']
        diagnostico.falla_encontrada = resultado['falla_encontrada']
        diagnostico.recomendaciones = resultado['recomendaciones']
        diagnostico.reglas_aplicadas = resultado.get('reglas_detalle', [])
        diagnostico.confianza = resultado['confianza']
        diagnostico.tiempo_respuesta = tiempo_respuesta
        diagnostico.save()

        return JsonResponse({
            'success': True,
            'diagnostico_id': diagnostico.id,
            'resultado': resultado,
        })

    except Exception as e:
        logger.error(f"Error en diagnosticar_rapido: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


def obtener_preguntas_api(request):
    sintoma = request.GET.get('sintoma', '')
    if sintoma:
        preguntas = motor.generar_preguntas(sintoma)
    else:
        preguntas = preguntas_mgr.obtener_todas()

    return JsonResponse({'preguntas': preguntas})


def obtener_sintomas_api(request):
    sintomas = base_cono.obtener_todos_sintomas()
    return JsonResponse({'sintomas': sintomas})


@require_POST
def nuevo_diagnostico_api(request):
    try:
        data = json.loads(request.body)
        sintoma_principal = data.get('sintoma_principal', '')

        diagnostico = Diagnostico.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            sesion_id=request.session.session_key or '',
            estado='en_curso',
            sintomas={'sintoma_principal': sintoma_principal},
        )

        preguntas = motor.generar_preguntas(sintoma_principal)
        request.session['diagnostico_activo'] = diagnostico.id
        request.session['preguntas_diagnostico'] = [p['id'] for p in preguntas]
        request.session['pregunta_actual_idx'] = 0

        return JsonResponse({
            'success': True,
            'diagnostico_id': diagnostico.id,
            'preguntas': preguntas,
        })

    except Exception as e:
        logger.error(f"Error en nuevo_diagnostico_api: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
