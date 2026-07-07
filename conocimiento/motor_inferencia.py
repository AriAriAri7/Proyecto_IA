import logging
from conocimiento.reglas import ReglasManager
from conocimiento.base_conocimiento import BaseConocimiento

logger = logging.getLogger('conocimiento')


class FallasKnowledgeEngine:
    def __init__(self):
        self.reglas_manager = ReglasManager()
        self.base_conocimiento = BaseConocimiento()
        self.diagnostico_resultado = None
        self.reglas_activadas = []
        self.hechos_recopilados = {}

    def inicializar(self):
        self.hechos_recopilados = {}
        self.reglas_activadas = []
        self.diagnostico_resultado = None
        logger.info("Motor de inferencia inicializado correctamente")

    def agregar_hecho(self, clave, valor):
        self.hechos_recopilados[clave] = valor
        logger.info(f"Hecho agregado: {clave} = {valor}")

    def agregar_hechos_multiples(self, hechos_dict):
        for clave, valor in hechos_dict.items():
            self.agregar_hecho(clave, valor)

    def _evaluar_reglas(self):
        reglas = self.reglas_manager.obtener_todas()
        activadas = []

        for regla in reglas:
            cumple = True
            for cond_clave, cond_valor in regla['condiciones'].items():
                hecho_valor = self.hechos_recopilados.get(cond_clave)
                if hecho_valor != cond_valor:
                    cumple = False
                    break
            if cumple:
                activadas.append(regla)
                logger.info(f"Regla activada: {regla['id']} - {regla['nombre']}")

        activadas.sort(key=lambda r: r['prioridad'])
        return activadas

    def inferir(self, hechos_usuario=None):
        self.inicializar()

        if hechos_usuario:
            for clave, valor in hechos_usuario.items():
                if valor is not None and valor != '':
                    self.hechos_recopilados[clave] = valor

        logger.info(f"Iniciando inferencia con hechos: {self.hechos_recopilados}")

        reglas_activadas = self._evaluar_reglas()
        self.reglas_activadas = reglas_activadas

        if not reglas_activadas:
            self.diagnostico_resultado = self._generar_diagnostico_generico()
            logger.warning("No se activaron reglas especificas, generando diagnostico generico")
            return self.diagnostico_resultado

        mejor_regla = reglas_activadas[0]
        falla_id = mejor_regla['conclusion']
        falla = self.base_conocimiento.obtener_falla(falla_id)
        recomendaciones = self.base_conocimiento.obtener_recomendaciones(falla_id)

        self.diagnostico_resultado = {
            'falla_encontrada': falla_id,
            'nombre_falla': falla['nombre'] if falla else 'Falla no identificada',
            'descripcion': falla['descripcion'] if falla else 'No se pudo determinar la falla especifica.',
            'gravedad': falla['gravedad'] if falla else 'medio',
            'icono': falla['icono'] if falla else 'question-circle',
            'tiempo_reparacion': falla.get('tiempo_reparacion', 'No estimado') if falla else 'No estimado',
            'reglas_activadas': [r['id'] for r in reglas_activadas],
            'reglas_detalle': [
                {
                    'id': r['id'],
                    'nombre': r['nombre'],
                    'explicacion': r.get('explicacion', ''),
                    'acciones': r.get('acciones', [])
                } for r in reglas_activadas
            ],
            'recomendaciones': recomendaciones,
            'confianza': self._calcular_confianza(reglas_activadas),
            'hechos_evaluados': dict(self.hechos_recopilados)
        }

        logger.info(f"Diagnostico completado: {self.diagnostico_resultado['nombre_falla']} "
                     f"(confianza: {self.diagnostico_resultado['confianza']}%)")
        return self.diagnostico_resultado

    def _generar_diagnostico_generico(self):
        return {
            'falla_encontrada': 'no_determinada',
            'nombre_falla': 'No se pudo determinar la falla especifica',
            'descripcion': 'Con la informacion proporcionada no fue posible identificar una falla especifica. '
                          'Se recomienda realizar un diagnostico mas detallado o consultar con un tecnico especializado.',
            'gravedad': 'bajo',
            'icono': 'question-circle',
            'tiempo_reparacion': 'No estimado',
            'reglas_activadas': [],
            'reglas_detalle': [],
            'recomendaciones': [
                'Revisa que todos los cables esten bien conectados.',
                'Verifica que el equipo reciba alimentacion electrica.',
                'Intenta reiniciar el equipo completamente.',
                'Si el problema persiste, contacta a un tecnico especializado.'
            ],
            'confianza': 0,
            'hechos_evaluados': dict(self.hechos_recopilados)
        }

    def _calcular_confianza(self, reglas):
        if not reglas:
            return 0
        puntuacion = 0
        for r in reglas:
            num_cond = len(r['condiciones'])
            prioridad = r['prioridad']
            puntuacion += (1.0 / num_cond) * (20.0 / prioridad)
        return min(100, int(puntuacion * 100))

    def generar_preguntas(self, sintoma_principal=None):
        from conocimiento.preguntas import PreguntasManager
        pm = PreguntasManager()

        if sintoma_principal:
            flujo_map = {
                'no_enciende': 'no_enciende',
                'pantalla_negra': 'pantalla_anormal',
                'pantalla_azul': 'pantalla_azul',
                'ruidos_extranos': 'ruidos',
                'calor_excesivo': 'sobrecalentamiento',
                'sistema_lento': 'lentitud',
                'sin_internet': 'internet',
            }
            flujo_key = flujo_map.get(sintoma_principal, 'por_defecto')
            preguntas_ids = pm.flujo.get(flujo_key, pm.flujo['por_defecto'])
            return [pm.obtener_pregunta(pid) for pid in preguntas_ids if pm.obtener_pregunta(pid)]

        preguntas = pm.obtener_todas()
        respondidas = set(self.hechos_recopilados.keys())

        return [p for p in preguntas if p['variable'] not in respondidas]
