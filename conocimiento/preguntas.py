class PreguntasManager:
    def __init__(self):
        self.preguntas = self._get_preguntas()
        self.flujo = self._get_flujo_preguntas()

    def _get_preguntas(self):
        return [
            {
                "id": "P001",
                "pregunta": "El equipo enciende cuando presionas el boton de encendido?",
                "variable": "no_enciende",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "Si, enciende normalmente"},
                    {"valor": True, "etiqueta": "No enciende"},
                    {"valor": False, "etiqueta": "Enciende pero se apaga"}
                ],
                "categoria": "encendido",
                "siguiente": None
            },
            {
                "id": "P002",
                "pregunta": "Que tipo de pantalla ves cuando enciendes el equipo?",
                "variable": "pantalla_negra",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "Pantalla normal con Windows"},
                    {"valor": True, "etiqueta": "Pantalla negra, no se ve nada"},
                    {"valor": "azul", "etiqueta": "Pantalla azul con texto blanco"},
                    {"valor": "congelada", "etiqueta": "Pantalla congelada, no responde"}
                ],
                "categoria": "pantalla",
                "siguiente": None
            },
            {
                "id": "P003",
                "pregunta": "Escuchas algun pitido al encender el equipo?",
                "variable": "pitidos_continuos",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, solo se escucha el ventilador"},
                    {"valor": True, "etiqueta": "Si, pitidos continuos y repetitivos"},
                    {"valor": "aislados", "etiqueta": "Si, pero solo uno o dos pitidos cortos"}
                ],
                "categoria": "pitidos",
                "siguiente": None
            },
            {
                "id": "P004",
                "pregunta": "Escuchas ruidos extranos provenientes del equipo?",
                "variable": "ruidos_extranos",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, todo suena normal"},
                    {"valor": True, "etiqueta": "Si, se escuchan clics o rechinidos"},
                    {"valor": True, "etiqueta": "Si, el ventilador suena muy fuerte"}
                ],
                "categoria": "ruidos",
                "siguiente": None
            },
            {
                "id": "P005",
                "pregunta": "Sientes que el equipo se calienta demasiado?",
                "variable": "calor_excesivo",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, la temperatura es normal"},
                    {"valor": True, "etiqueta": "Si, el equipo quema al tacto"},
                    {"valor": True, "etiqueta": "Un poco mas de lo normal"}
                ],
                "categoria": "temperatura",
                "siguiente": None
            },
            {
                "id": "P006",
                "pregunta": "El equipo se apaga solo sin previo aviso?",
                "variable": "se_apaga_solo",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, se mantiene encendido"},
                    {"valor": True, "etiqueta": "Si, se apaga de repente"},
                    {"valor": True, "etiqueta": "Se reinicia solo constantemente"}
                ],
                "categoria": "comportamiento",
                "siguiente": None
            },
            {
                "id": "P007",
                "pregunta": "Has instalado algun programa o actualizacion recientemente?",
                "variable": "instalacion_reciente",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, no he instalado nada nuevo"},
                    {"valor": True, "etiqueta": "Si, instale un programa"},
                    {"valor": True, "etiqueta": "Si, Windows se actualizo"}
                ],
                "categoria": "cambios",
                "siguiente": None
            },
            {
                "id": "P008",
                "pregunta": "El equipo se siente lento al usarlo?",
                "variable": "sistema_lento",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, funciona con normalidad"},
                    {"valor": True, "etiqueta": "Si, esta muy lento"},
                    {"valor": True, "etiqueta": "A veces se congela unos segundos"}
                ],
                "categoria": "rendimiento",
                "siguiente": None
            },
            {
                "id": "P009",
                "pregunta": "Aparecen ventanas emergentes o anuncios sin que abras nada?",
                "variable": "ventanas_emergentes",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, no veo nada extrano"},
                    {"valor": True, "etiqueta": "Si, aparecen muchos anuncios"},
                    {"valor": True, "etiqueta": "Si, y se abren paginas web solas"}
                ],
                "categoria": "software",
                "siguiente": None
            },
            {
                "id": "P010",
                "pregunta": "Tienes conexion a Internet?",
                "variable": "sin_internet",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "Si, tengo Internet normal"},
                    {"valor": True, "etiqueta": "No tengo Internet"},
                    {"valor": True, "etiqueta": "Se conecta pero no navega"}
                ],
                "categoria": "red",
                "siguiente": None
            },
            {
                "id": "P011",
                "pregunta": "Los dispositivos conectados (mouse, teclado, impresora) funcionan bien?",
                "variable": "perifericos_no_funcionan",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "Si, funcionan correctamente"},
                    {"valor": True, "etiqueta": "No, algunos no funcionan"},
                    {"valor": True, "etiqueta": "Funcionan pero a veces se desconectan"}
                ],
                "categoria": "perifericos",
                "siguiente": None
            },
            {
                "id": "P012",
                "pregunta": "Has realizado limpieza o mantenimiento al equipo recientemente?",
                "variable": "sin_mantenimiento",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "Si, lo limpio regularmente"},
                    {"valor": True, "etiqueta": "No, nunca lo he limpiado"},
                    {"valor": True, "etiqueta": "Tiene mas de un ano sin limpieza"}
                ],
                "categoria": "mantenimiento",
                "siguiente": None
            },
            {
                "id": "P013",
                "pregunta": "La fuente de poder hace ruido o se siente muy caliente?",
                "variable": "fuente_poder_ruidosa",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, funciona silenciosamente"},
                    {"valor": True, "etiqueta": "Si, se escucha un zumbido"},
                    {"valor": True, "etiqueta": "Si, la fuente quema al tacto"}
                ],
                "categoria": "fuente",
                "siguiente": None
            },
            {
                "id": "P014",
                "pregunta": "Aparece un codigo de error en la pantalla azul?",
                "variable": "codigo_error_7B",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No se ve ningun codigo"},
                    {"valor": True, "etiqueta": "Si, dice 0x0000007B"},
                    {"valor": False, "etiqueta": "Tiene otro codigo diferente"}
                ],
                "categoria": "pantalla",
                "siguiente": None
            },
            {
                "id": "P015",
                "pregunta": "El equipo se reinicia solo frecuentemente?",
                "variable": "reinicios_frecuentes",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, se mantiene estable"},
                    {"valor": True, "etiqueta": "Si, se reinicia solo"},
                    {"valor": True, "etiqueta": "Se reinicia al hacer algo especifico"}
                ],
                "categoria": "comportamiento",
                "siguiente": None
            },
            {
                "id": "P016",
                "pregunta": "El boton de encendido se siente normal o esta muy suelto/duro?",
                "variable": "boton_encendido_suave",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "Normal, hace clic al presionarlo"},
                    {"valor": True, "etiqueta": "Esta muy suelto o no hace clic"},
                    {"valor": True, "etiqueta": "Esta muy duro o atascado"}
                ],
                "categoria": "encendido",
                "siguiente": None
            },
            {
                "id": "P017",
                "pregunta": "Has notado programas que no reconoces en el equipo?",
                "variable": "programas_extranos",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, todos son conocidos"},
                    {"valor": True, "etiqueta": "Si, hay programas que no instale"},
                    {"valor": True, "etiqueta": "Si, la pagina de inicio cambio sola"}
                ],
                "categoria": "software",
                "siguiente": None
            },
            {
                "id": "P018",
                "pregunta": "Windows inicia normalmente o muestra mensajes de error al arrancar?",
                "variable": "no_inicia_windows",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "Windows inicia con normalidad"},
                    {"valor": True, "etiqueta": "No inicia, se queda cargando"},
                    {"valor": True, "etiqueta": "Muestra pantalla negra con cursor"}
                ],
                "categoria": "sistema",
                "siguiente": None
            },
            {
                "id": "P019",
                "pregunta": "Has realizado cambios en la configuracion de red recientemente?",
                "variable": "configuracion_cambiada",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, no he cambiado nada"},
                    {"valor": True, "etiqueta": "Si, cambie la contrasena del WiFi"},
                    {"valor": True, "etiqueta": "Si, instale un nuevo router"}
                ],
                "categoria": "red",
                "siguiente": None
            },
            {
                "id": "P020",
                "pregunta": "Crees que el equipo tiene suficiente memoria RAM para lo que haces?",
                "variable": "ram_insuficiente",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "Si, tengo suficiente memoria"},
                    {"valor": True, "etiqueta": "No, siempre esta al maximo"},
                    {"valor": True, "etiqueta": "No estoy seguro, pero va muy lento"}
                ],
                "categoria": "rendimiento",
                "siguiente": None
            },
            {
                "id": "P021",
                "pregunta": "El WiFi aparece desconectado o no se ve ninguna red?",
                "variable": "wifi_desconectado",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "Veo redes WiFi disponibles"},
                    {"valor": True, "etiqueta": "No veo ninguna red WiFi"},
                    {"valor": True, "etiqueta": "El icono de WiFi aparece con una X"}
                ],
                "categoria": "red",
                "siguiente": None
            },
            {
                "id": "P022",
                "pregunta": "El equipo se congela o queda sin respuesta al abrir varios programas?",
                "variable": "congelamientos",
                "tipo": "select",
                "opciones": [
                    {"valor": False, "etiqueta": "No, funciona bien con varios programas"},
                    {"valor": True, "etiqueta": "Si, se congela con varios programas abiertos"},
                    {"valor": True, "etiqueta": "Si, a veces no responde por varios segundos"}
                ],
                "categoria": "rendimiento",
                "siguiente": None
            }
        ]

    def _get_flujo_preguntas(self):
        return {
            "inicial": "P001",
            "no_enciende": ["P001", "P003", "P016", "P013"],
            "pantalla_anormal": ["P002", "P003", "P007", "P014"],
            "ruidos": ["P004", "P005", "P012", "P013"],
            "lentitud": ["P008", "P009", "P017", "P020", "P022"],
            "internet": ["P010", "P019", "P021"],
            "perifericos": ["P011", "P007"],
            "sobrecalentamiento": ["P005", "P006", "P012", "P004", "P013"],
            "pantalla_azul": ["P002", "P007", "P014", "P015", "P018"],
            "por_defecto": ["P001", "P002", "P003", "P004", "P005", "P006", "P008"]
        }

    def obtener_pregunta(self, pregunta_id):
        for p in self.preguntas:
            if p['id'] == pregunta_id:
                return p
        return None

    def obtener_pregunta_inicial(self):
        return self.obtener_pregunta("P001")

    def obtener_siguientes(self, pregunta_id, respuesta=None):
        pregunta = self.obtener_pregunta(pregunta_id)
        if not pregunta:
            return []
        flujo_key = self._determinar_flujo(pregunta, respuesta)
        ids_preguntas = self.flujo.get(flujo_key, self.flujo["por_defecto"])
        idx = ids_preguntas.index(pregunta_id) if pregunta_id in ids_preguntas else -1
        if idx >= 0 and idx + 1 < len(ids_preguntas):
            siguiente_id = ids_preguntas[idx + 1]
            return [self.obtener_pregunta(siguiente_id)]
        return []

    def _determinar_flujo(self, pregunta, respuesta):
        mapeo = {
            "no_enciende": "no_enciende",
            "pantalla_negra": "pantalla_anormal",
            "pantalla_azul": "pantalla_azul",
            "ruidos_extranos": "ruidos",
            "calor_excesivo": "sobrecalentamiento",
            "sistema_lento": "lentitud",
            "sin_internet": "internet",
            "perifericos_no_funcionan": "perifericos",
        }
        variable = pregunta.get('variable', '')
        return mapeo.get(variable, "por_defecto")

    def obtener_todas(self):
        return self.preguntas
