import json
import os
from pathlib import Path


class ReglasManager:
    def __init__(self):
        self.reglas = self._cargar_reglas()
        self.reglas_predefinidas = self._get_reglas_predefinidas()

    def _cargar_reglas(self):
        ruta_json = Path(__file__).resolve().parent / 'reglas.json'
        if ruta_json.exists():
            try:
                with open(ruta_json, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _get_reglas_predefinidas(self):
        return [
            {
                "id": "R001",
                "nombre": "Falla de fuente de poder",
                "categoria": "hardware",
                "condiciones": {"no_enciende": True, "sin_luces": True, "sin_ventiladores": True},
                "conclusion": "falla_fuente_poder",
                "acciones": ["Revisar cable de alimentacion", "Probar con otra fuente de poder", "Verificar regulador de voltaje"],
                "prioridad": 1,
                "explicacion": "El equipo no enciende, no hay luces ni ventiladores funcionando. Esto indica que la fuente de poder no esta suministrando energia."
            },
            {
                "id": "R002",
                "nombre": "Falla de memoria RAM",
                "categoria": "hardware",
                "condiciones": {"pitidos_continuos": True, "pantalla_negra": True},
                "conclusion": "falla_memoria_ram",
                "acciones": ["Limpiar contactos de la RAM con borrador", "Reinsertar los modulos de memoria", "Probar cada modulo por separado", "Reemplazar modulo danado"],
                "prioridad": 2,
                "explicacion": "Los pitidos continuos y la pantalla negra son sintomas clasicos de falla en la memoria RAM."
            },
            {
                "id": "R003",
                "nombre": "Sobrecalentamiento",
                "categoria": "hardware",
                "condiciones": {"se_apaga_solo": True, "calor_excesivo": True},
                "conclusion": "sobrecalentamiento",
                "acciones": ["Limpiar el polvo de los ventiladores", "Verificar que los ventiladores giren libremente", "Aplicar nueva pasta termica al procesador", "Mejorar ventilacion del gabinete"],
                "prioridad": 3,
                "explicacion": "El equipo se apaga solo y se siente muy caliente. El sobrecalentamiento puede danar componentes internos."
            },
            {
                "id": "R004",
                "nombre": "Conflicto de controladores",
                "categoria": "software",
                "condiciones": {"pantalla_azul": True, "instalacion_reciente": True},
                "conclusion": "conflicto_controladores",
                "acciones": ["Ingresar a modo seguro", "Desinstalar controladores recien instalados", "Restaurar sistema a un punto anterior", "Descargar controladores oficiales"],
                "prioridad": 4,
                "explicacion": "La pantalla azul despues de una instalacion reciente sugiere conflicto con controladores nuevos."
            },
            {
                "id": "R005",
                "nombre": "Falla de disco duro o SSD",
                "categoria": "hardware",
                "condiciones": {"ruidos_extranos": True, "sistema_lento": True},
                "conclusion": "falla_disco_duro",
                "acciones": ["Realizar backup inmediato de datos", "Ejecutar revisacion de disco (CHKDSK)", "Verificar estado SMART del disco", "Reemplazar disco danado"],
                "prioridad": 5,
                "explicacion": "Ruidos extranos (clics, rechinidos) combinados con lentitud indican falla mecanica inminente del disco."
            },
            {
                "id": "R006",
                "nombre": "Falla de tarjeta de video",
                "categoria": "hardware",
                "condiciones": {"pantalla_negra": True, "ventiladores_funcionan": True, "sin_pitidos": True},
                "conclusion": "falla_tarjeta_video",
                "acciones": ["Verificar que el monitor este encendido y conectado", "Reinsertar tarjeta de video", "Probar con otro monitor o cable", "Reemplazar tarjeta de video si es necesario"],
                "prioridad": 6,
                "explicacion": "El equipo enciende (ventiladores giran, no hay pitidos) pero la pantalla permanece negra. La tarjeta de video podria estar fallando."
            },
            {
                "id": "R007",
                "nombre": "Dano en sistema operativo",
                "categoria": "software",
                "condiciones": {"pantalla_azul": True, "reinicios": True, "sin_cambios": True},
                "conclusion": "falla_sistema_operativo",
                "acciones": ["Intentar reparacion de inicio", "Ejecutar restaurar sistema", "Realizar reparacion con disco de instalacion", "Reinstalar sistema operativo"],
                "prioridad": 7,
                "explicacion": "Pantallazos azules y reinicios sin haber realizado cambios recientes indican corrupcion del sistema operativo."
            },
            {
                "id": "R008",
                "nombre": "Infeccion por malware",
                "categoria": "software",
                "condiciones": {"sistema_lento": True, "ventanas_emergentes": True},
                "conclusion": "infeccion_malware",
                "acciones": ["Ejecutar antivirus en modo seguro", "Usar Windows Defender para analisis completo", "Usar herramientas antimalware (Malwarebytes)", "Eliminar archivos temporales", "Restaurar navegador a configuracion predeterminada"],
                "prioridad": 8,
                "explicacion": "La lentitud extrema combinada con ventanas emergentes y anuncios son sintomas clasicos de infeccion por malware."
            },
            {
                "id": "R009",
                "nombre": "Falla de ventiladores",
                "categoria": "hardware",
                "condiciones": {"ruidos_extranos": True, "calor_excesivo": True},
                "conclusion": "falla_ventilador",
                "acciones": ["Limpiar los ventiladores con aire comprimido", "Verificar que los ventiladores giren libremente", "Lubricar los ventiladores si es posible", "Reemplazar ventiladores defectuosos"],
                "prioridad": 9,
                "explicacion": "Ruidos extranos y sobrecalentamiento indican que los ventiladores no estan funcionando correctamente."
            },
            {
                "id": "R010",
                "nombre": "Problema de conexion a Internet",
                "categoria": "red",
                "condiciones": {"sin_internet": True, "configuracion_cambiada": True},
                "conclusion": "problema_red",
                "acciones": ["Reiniciar modem y router", "Verificar cable de red o WiFi", "Ejecutar solucion de problemas de red", "Restablecer configuracion de red", "Contactar al proveedor de Internet"],
                "prioridad": 10,
                "explicacion": "La perdida de Internet luego de cambios en la configuracion sugiere un problema de configuracion de red."
            },
            {
                "id": "R011",
                "nombre": "Problema con perifericos",
                "categoria": "software",
                "condiciones": {"perifericos_no_funcionan": True, "controladores_viejos": True},
                "conclusion": "problema_controladores",
                "acciones": ["Reconectar el dispositivo", "Probar en otro puerto USB", "Actualizar controladores desde Administrador de dispositivos", "Reinstalar controladores del fabricante"],
                "prioridad": 11,
                "explicacion": "Los perifericos no funcionan correctamente debido a controladores desactualizados o corruptos."
            },
            {
                "id": "R012",
                "nombre": "Falla de fuente de poder (reinicios)",
                "categoria": "hardware",
                "condiciones": {"reinicios_frecuentes": True, "fuente_poder_ruidosa": True},
                "conclusion": "falla_fuente_poder",
                "acciones": ["Verificar que la fuente tenga la potencia adecuada", "Revisar conexiones internas de la fuente", "Probar con una fuente de poder de repuesto", "Reemplazar fuente de poder danada"],
                "prioridad": 12,
                "explicacion": "Los reinicios frecuentes combinados con ruidos provenientes de la fuente indican que esta fallando."
            },
            {
                "id": "R013",
                "nombre": "Falla de disco duro (BSOD)",
                "categoria": "hardware",
                "condiciones": {"pantalla_azul": True, "codigo_error_7B": True},
                "conclusion": "falla_disco_duro",
                "acciones": ["Revisar conexiones del disco duro", "Ejecutar CHKDSK desde consola de recuperacion", "Verificar estado del disco con herramientas S.M.A.R.T.", "Reemplazar disco duro defectuoso"],
                "prioridad": 13,
                "explicacion": "El codigo de error 0x0000007B en pantalla azul indica que Windows no puede acceder al disco de inicio."
            },
            {
                "id": "R014",
                "nombre": "Boton de encendido defectuoso",
                "categoria": "hardware",
                "condiciones": {"no_enciende": True, "boton_encendido_suave": True},
                "conclusion": "boton_defectuoso",
                "acciones": ["Verificar el boton de encendido del gabinete", "Probar encendiendo con un destornillador en los pines de la placa madre", "Reemplazar boton de encendido"],
                "prioridad": 14,
                "explicacion": "El boton de encendido se siente diferente (muy suave o atascado), lo que impide encender el equipo."
            },
            {
                "id": "R015",
                "nombre": "Memoria RAM insuficiente",
                "categoria": "hardware",
                "condiciones": {"congelamientos": True, "ram_insuficiente": True},
                "conclusion": "ram_insuficiente",
                "acciones": ["Cerrar programas innecesarios", "Agregar mas memoria RAM al equipo", "Aumentar memoria virtual de Windows", "Actualizar a un sistema operativo de 64 bits"],
                "prioridad": 15,
                "explicacion": "El equipo se congela frecuentemente y no tiene suficiente memoria RAM para las tareas actuales."
            },
            {
                "id": "R016",
                "nombre": "Problema de conexion WiFi",
                "categoria": "red",
                "condiciones": {"sin_internet": True, "wifi_desconectado": True},
                "conclusion": "problema_red",
                "acciones": ["Activar WiFi del equipo", "Olvidar y reconectar a la red WiFi", "Verificar contrasena de la red", "Reiniciar el router WiFi"],
                "prioridad": 16,
                "explicacion": "El equipo no tiene conexion a Internet y el WiFi aparece desconectado o no disponible."
            },
            {
                "id": "R017",
                "nombre": "Pantalla danada o cable de video",
                "categoria": "hardware",
                "condiciones": {"pantalla_negra": True, "ventiladores_funcionan": True, "pitidos_aislados": True},
                "conclusion": "falla_tarjeta_video",
                "acciones": ["Verificar cable de video (VGA/HDMI/DisplayPort)", "Probar con otro monitor", "Revisar que la tarjeta de video este bien insertada", "Actualizar controladores de video en modo seguro"],
                "prioridad": 17,
                "explicacion": "La pantalla permanece negra aunque el equipo enciende. Podria ser el cable de video o la tarjeta grafica."
            },
            {
                "id": "R018",
                "nombre": "Sistema operativo corrupto",
                "categoria": "software",
                "condiciones": {"no_inicia_windows": True, "archivos_corruptos": True},
                "conclusion": "falla_sistema_operativo",
                "acciones": ["Ejecutar reparacion automatica de inicio", "Usar simbolo del sistema para reparar archivos (SFC /SCANNOW)", "Restaurar sistema desde punto de restauracion", "Reinstalar Windows conservando archivos"],
                "prioridad": 18,
                "explicacion": "Windows no inicia correctamente y muestra mensajes de archivos corruptos o faltantes."
            },
            {
                "id": "R019",
                "nombre": "Problema de temperatura ambiente",
                "categoria": "hardware",
                "condiciones": {"calor_excesivo": True, "sin_mantenimiento": True},
                "conclusion": "sobrecalentamiento",
                "acciones": ["Ubicar el equipo en un lugar ventilado", "Limpiar el polvo acumulado", "Verificar que las rejillas de ventilacion no esten obstruidas", "Usar base refrigeradora para laptops"],
                "prioridad": 19,
                "explicacion": "La falta de mantenimiento y la acumulacion de polvo causan sobrecalentamiento del equipo."
            },
            {
                "id": "R020",
                "nombre": "Infeccion por virus",
                "categoria": "software",
                "condiciones": {"sistema_lento": True, "programas_extraños": True},
                "conclusion": "infeccion_malware",
                "acciones": ["Ejecutar analisis completo con Windows Defender", "Usar herramienta de eliminacion de software malicioso", "Revisar programas en inicio", "Restablecer el equipo si es necesario"],
                "prioridad": 20,
                "explicacion": "La presencia de programas desconocidos y lentitud general son indicadores de infeccion por malware."
            }
        ]

    def obtener_todas(self):
        return self.reglas_predefinidas

    def obtener_por_id(self, regla_id):
        for regla in self.reglas_predefinidas:
            if regla['id'] == regla_id:
                return regla
        return None

    def obtener_por_categoria(self, categoria):
        return [r for r in self.reglas_predefinidas if r['categoria'] == categoria]

    def obtener_activas(self):
        return [r for r in self.reglas_predefinidas if r.get('activa', True)]

    def validar_condiciones(self, regla, hechos):
        for clave, valor in regla['condiciones'].items():
            if hechos.get(clave) != valor:
                return False
        return True
