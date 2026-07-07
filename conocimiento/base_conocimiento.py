class BaseConocimiento:
    def __init__(self):
        self.sintomas = self._get_sintomas()
        self.fallas = self._get_fallas()
        self.recomendaciones = self._get_recomendaciones()
        self.mapeo_sintomas_fallas = self._get_mapeo_sintomas_fallas()

    def _get_sintomas(self):
        return {
            "no_enciende": {"nombre": "No enciende", "descripcion": "El equipo no responde al presionar el boton de encendido", "categoria": "encendido", "gravedad": "critico"},
            "pantalla_negra": {"nombre": "Pantalla negra", "descripcion": "El equipo enciende pero la pantalla se queda en negro", "categoria": "pantalla", "gravedad": "critico"},
            "pantalla_azul": {"nombre": "Pantalla azul (BSOD)", "descripcion": "Aparece pantalla azul con texto blanco", "categoria": "pantalla", "gravedad": "critico"},
            "pitidos_continuos": {"nombre": "Pitidos al encender", "descripcion": "Se escuchan pitidos al presionar el boton de encendido", "categoria": "arranque", "gravedad": "critico"},
            "ruidos_extranos": {"nombre": "Ruidos extranos", "descripcion": "Se escuchan clics, rechinidos o zumbidos", "categoria": "hardware", "gravedad": "medio"},
            "calor_excesivo": {"nombre": "Sobrecalentamiento", "descripcion": "El equipo se siente muy caliente al tacto", "categoria": "temperatura", "gravedad": "critico"},
            "sistema_lento": {"nombre": "Sistema lento", "descripcion": "El equipo funciona muy lento o se congela", "categoria": "rendimiento", "gravedad": "medio"},
            "se_apaga_solo": {"nombre": "Se apaga solo", "descripcion": "El equipo se apaga o reinicia sin previo aviso", "categoria": "comportamiento", "gravedad": "critico"},
            "ventanas_emergentes": {"nombre": "Ventanas emergentes", "descripcion": "Aparecen anuncios o ventanas sin abrir nada", "categoria": "software", "gravedad": "bajo"},
            "sin_internet": {"nombre": "Sin Internet", "descripcion": "El equipo no tiene conexion a Internet", "categoria": "red", "gravedad": "medio"},
            "perifericos_no_funcionan": {"nombre": "Perifericos no funcionan", "descripcion": "Mouse, teclado u otros dispositivos no responden", "categoria": "hardware", "gravedad": "medio"},
            "instalacion_reciente": {"nombre": "Instalacion reciente", "descripcion": "Se instalo un programa o actualizacion recientemente", "categoria": "software", "gravedad": "bajo"},
            "reinicios_frecuentes": {"nombre": "Reinicios frecuentes", "descripcion": "El equipo se reinicia constantemente", "categoria": "comportamiento", "gravedad": "critico"},
            "fuente_poder_ruidosa": {"nombre": "Fuente ruidosa", "descripcion": "La fuente de poder hace ruido o esta muy caliente", "categoria": "hardware", "gravedad": "critico"},
            "codigo_error_7B": {"nombre": "Error 0x0000007B", "descripcion": "Pantalla azul con codigo 0x0000007B", "categoria": "pantalla", "gravedad": "critico"},
            "boton_encendido_suave": {"nombre": "Boton defectuoso", "descripcion": "El boton de encendido se siente extrano", "categoria": "encendido", "gravedad": "medio"},
            "sin_mantenimiento": {"nombre": "Sin mantenimiento", "descripcion": "El equipo no ha recibido limpieza o mantenimiento", "categoria": "mantenimiento", "gravedad": "bajo"},
            "ram_insuficiente": {"nombre": "RAM insuficiente", "descripcion": "La memoria RAM es insuficiente para las tareas", "categoria": "rendimiento", "gravedad": "medio"},
            "no_inicia_windows": {"nombre": "Windows no inicia", "descripcion": "Windows no arranca o se queda cargando", "categoria": "sistema", "gravedad": "critico"},
            "configuracion_cambiada": {"nombre": "Configuracion cambiada", "descripcion": "Se modifico la configuracion de red o sistema", "categoria": "red", "gravedad": "bajo"},
        }

    def _get_fallas(self):
        return {
            "falla_fuente_poder": {
                "nombre": "Falla en la Fuente de Poder",
                "descripcion": "La fuente de poder no esta suministrando energia correctamente al equipo.",
                "icono": "power-off",
                "gravedad": "critico",
                "tiempo_reparacion": "1-2 horas"
            },
            "falla_memoria_ram": {
                "nombre": "Falla en la Memoria RAM",
                "descripcion": "Uno o mas modulos de memoria RAM estan fallando o mal colocados.",
                "icono": "microchip",
                "gravedad": "critico",
                "tiempo_reparacion": "30-60 minutos"
            },
            "sobrecalentamiento": {
                "nombre": "Sobrecalentamiento del Equipo",
                "descripcion": "El equipo esta alcanzando temperaturas peligrosas para sus componentes.",
                "icono": "thermometer-high",
                "gravedad": "critico",
                "tiempo_reparacion": "1-3 horas"
            },
            "conflicto_controladores": {
                "nombre": "Conflicto de Controladores",
                "descripcion": "Los controladores de dispositivos estan en conflicto con el sistema.",
                "icono": "exclamation-triangle",
                "gravedad": "medio",
                "tiempo_reparacion": "30-60 minutos"
            },
            "falla_disco_duro": {
                "nombre": "Falla en Disco Duro o SSD",
                "descripcion": "El disco duro presenta fallas fisicas o logicas que afectan el rendimiento.",
                "icono": "hdd",
                "gravedad": "critico",
                "tiempo_reparacion": "2-4 horas"
            },
            "falla_tarjeta_video": {
                "nombre": "Falla en Tarjeta de Video",
                "descripcion": "La tarjeta grafica no esta enviando senal al monitor.",
                "icono": "video",
                "gravedad": "critico",
                "tiempo_reparacion": "1-3 horas"
            },
            "falla_sistema_operativo": {
                "nombre": "Dano en el Sistema Operativo",
                "descripcion": "El sistema operativo Windows esta danado o corrupto.",
                "icono": "windows",
                "gravedad": "critico",
                "tiempo_reparacion": "2-4 horas"
            },
            "infeccion_malware": {
                "nombre": "Infeccion por Malware o Virus",
                "descripcion": "El equipo esta infectado con software malicioso.",
                "icono": "bug",
                "gravedad": "medio",
                "tiempo_reparacion": "1-3 horas"
            },
            "falla_ventilador": {
                "nombre": "Falla en Ventiladores",
                "descripcion": "Los ventiladores del equipo no estan funcionando correctamente.",
                "icono": "fan",
                "gravedad": "medio",
                "tiempo_reparacion": "30-60 minutos"
            },
            "problema_red": {
                "nombre": "Problema de Conexion de Red",
                "descripcion": "El equipo tiene problemas para conectarse a Internet o la red local.",
                "icono": "wifi",
                "gravedad": "medio",
                "tiempo_reparacion": "30-60 minutos"
            },
            "problema_controladores": {
                "nombre": "Problema con Controladores de Perifericos",
                "descripcion": "Los controladores de dispositivos externos estan desactualizados o corruptos.",
                "icono": "usb",
                "gravedad": "bajo",
                "tiempo_reparacion": "15-30 minutos"
            },
            "boton_defectuoso": {
                "nombre": "Boton de Encendido Defectuoso",
                "descripcion": "El boton de encendido del gabinete esta danado o atascado.",
                "icono": "toggle-off",
                "gravedad": "bajo",
                "tiempo_reparacion": "30-60 minutos"
            },
            "ram_insuficiente": {
                "nombre": "Memoria RAM Insuficiente",
                "descripcion": "La cantidad de memoria RAM instalada no es suficiente para las tareas actuales.",
                "icono": "memory",
                "gravedad": "medio",
                "tiempo_reparacion": "30-60 minutos"
            }
        }

    def _get_recomendaciones(self):
        return {
            "falla_fuente_poder": [
                "Verifica que el cable de alimentacion este bien conectado tanto al equipo como a la toma electrica.",
                "Prueba conectando el equipo a otra toma de corriente para descartar problemas electricos.",
                "Si tienes un regulador de voltaje o UPS, verifica que este encendido y funcionando.",
                "Si ninguno de los pasos anteriores funciona, es probable que la fuente de poder este danada y deba ser reemplazada por un tecnico especializado."
            ],
            "falla_memoria_ram": [
                "Apaga el equipo y desconectalo de la corriente electrica.",
                "Abre el gabinete y localiza los modulos de memoria RAM en la placa madre.",
                "Retira cada modulo de RAM y limpia los contactos dorados con una goma de borrar suavemente.",
                "Vuelve a colocar los modulos de RAM firmemente hasta que las pestanas hagan clic.",
                "Si tienes mas de un modulo, prueba cada uno por separado para identificar cual esta danado.",
                "Si el problema persiste, es necesario reemplazar el modulo de memoria defectuoso."
            ],
            "sobrecalentamiento": [
                "Apaga el equipo y desconectalo. Abre el gabinete y limpia el polvo acumulado con aire comprimido.",
                "Verifica que todos los ventiladores (procesador, gabinete, tarjeta de video) giren libremente.",
                "Si el procesador no tiene pasta termica o esta seca, aplica nueva pasta termica.",
                "Ubica el equipo en un lugar ventilado, lejos de paredes o muebles que obstruyan el flujo de aire.",
                "Para laptops, usa una base refrigeradora para mejorar la ventilacion."
            ],
            "conflicto_controladores": [
                "Reinicia el equipo e ingresa a Modo Seguro presionando F8 antes de que cargue Windows.",
                "Abre el Administrador de Dispositivos y busca dispositivos con un signo de admiracion amarillo.",
                "Desinstala los controladores de los dispositivos que instalaste recientemente.",
                "Usa la herramienta Restaurar Sistema para volver a un punto anterior donde el equipo funcionaba bien.",
                "Descarga e instala los controladores mas recientes desde la pagina oficial del fabricante."
            ],
            "falla_disco_duro": [
                "Realiza una copia de seguridad (backup) de tus archivos importantes inmediatamente.",
                "Abre el simbolo del sistema como administrador y ejecuta: chkdsk C: /f /r",
                "Descarga una herramienta para verificar el estado SMART del disco duro (como CrystalDiskInfo).",
                "Si el disco presenta sectores defectuosos o errores SMART, debe ser reemplazado.",
                "Acude a un tecnico especializado para la recuperacion de datos si es necesario."
            ],
            "falla_tarjeta_video": [
                "Verifica que el monitor este encendido y que el cable de video (VGA/HDMI/DisplayPort) este bien conectado.",
                "Prueba con otro monitor o cable de video para descartar problemas externos.",
                "Apaga el equipo, abre el gabinete y reinserta la tarjeta de video firmemente.",
                "Si tienes graficos integrados en la placa madre, conecta el monitor a ese puerto para probar.",
                "Si la tarjeta de video continua sin funcionar, probablemente deba ser reemplazada."
            ],
            "falla_sistema_operativo": [
                "Reinicia el equipo e intenta ingresar a las Opciones de Recuperacion de Windows.",
                "Selecciona Solucionar Problepos > Opciones Avanzadas > Reparacion de Inicio.",
                "Si no funciona, intenta Restaurar Sistema a un punto anterior.",
                "Ejecuta el simbolo del sistema y escribe: sfc /scannow para reparar archivos del sistema.",
                "Como ultima opcion, realiza una reinstalacion de Windows conservando tus archivos personales."
            ],
            "infeccion_malware": [
                "Reinicia el equipo en Modo Seguro con Red presionando F8 al iniciar.",
                "Ejecuta un analisis completo con Windows Defender o tu antivirus instalado.",
                "Usa herramientas especializadas como Malwarebytes o AdwCleaner para eliminar malware persistente.",
                "Elimina los archivos temporales con la herramienta Liberador de espacio en disco.",
                "Restablece la configuracion de tu navegador web a los valores predeterminados."
            ],
            "falla_ventilador": [
                "Apaga el equipo y desconectalo. Abre el gabinete y limpia los ventiladores con aire comprimido.",
                "Verifica que cada ventilador gire libremente. Si alguno esta atascado, intenta lubricarlo.",
                "Si el ventilador hace ruido pero gira, podria estar desgastado y necesitar reemplazo.",
                "Los ventiladores de computadora son economicos y faciles de reemplazar por un tecnico."
            ],
            "problema_red": [
                "Reinicia el modem y el router desconectandolos de la corriente por 30 segundos.",
                "Verifica que los cables de red esten bien conectados (si usas conexion por cable).",
                "Ejecuta el solucionador de problemas de red desde Configuracion de Windows.",
                "En el simbolo del sistema como administrador, ejecuta: ipconfig /release y luego ipconfig /renew",
                "Si nada funciona, contacta a tu proveedor de servicios de Internet."
            ],
            "problema_controladores": [
                "Desconecta y vuelve a conectar el dispositivo que no funciona.",
                "Prueba conectando el dispositivo en otro puerto USB del equipo.",
                "Abre el Administrador de Dispositivos, busca el dispositivo y selecciona Actualizar controlador.",
                "Si no se actualiza automaticamente, descarga el controlador desde la pagina del fabricante.",
                "Como ultimo recurso, desinstala el dispositivo y reinicia el equipo para que Windows lo reinstale."
            ],
            "boton_defectuoso": [
                "Verifica visualmente el boton de encendido del gabinete.",
                "Si el boton esta atascado, intenta liberarlo con cuidado usando un destornillador pequeno.",
                "Si el boton no hace contacto, se puede encender el equipo momentaneamente haciendo puente en los pines de la placa madre.",
                "Para una solucion permanente, reemplaza el boton de encendido o el gabinete."
            ],
            "ram_insuficiente": [
                "Cierra los programas que no estes usando para liberar memoria RAM.",
                "Abre el Administrador de Tareas (Ctrl+Shift+Esc) para ver que programas consumen mas memoria.",
                "Deshabilita programas que se inician automaticamente con Windows desde el Administrador de Tareas.",
                "Aumenta la memoria virtual de Windows: Configuracion > Sistema > Acerca de > Configuracion avanzada del sistema.",
                "Considera agregar modulos de memoria RAM adicionales a tu equipo para mejorar el rendimiento."
            ]
        }

    def _get_mapeo_sintomas_fallas(self):
        return {
            "no_enciende": ["falla_fuente_poder", "boton_defectuoso"],
            "pantalla_negra": ["falla_memoria_ram", "falla_tarjeta_video"],
            "pantalla_azul": ["conflicto_controladores", "falla_sistema_operativo", "falla_disco_duro"],
            "pitidos_continuos": ["falla_memoria_ram", "falla_tarjeta_video"],
            "ruidos_extranos": ["falla_disco_duro", "falla_ventilador"],
            "calor_excesivo": ["sobrecalentamiento", "falla_ventilador"],
            "sistema_lento": ["infeccion_malware", "falla_disco_duro", "ram_insuficiente"],
            "se_apaga_solo": ["sobrecalentamiento", "falla_fuente_poder"],
            "ventanas_emergentes": ["infeccion_malware"],
            "sin_internet": ["problema_red"],
            "perifericos_no_funcionan": ["problema_controladores"],
            "instalacion_reciente": ["conflicto_controladores"],
            "reinicios_frecuentes": ["falla_fuente_poder", "sobrecalentamiento"],
            "fuente_poder_ruidosa": ["falla_fuente_poder"],
            "codigo_error_7B": ["falla_disco_duro"],
            "boton_encendido_suave": ["boton_defectuoso"],
            "ram_insuficiente": ["ram_insuficiente"],
            "no_inicia_windows": ["falla_sistema_operativo"],
            "congelamientos": ["ram_insuficiente"],
        }

    def obtener_sintoma(self, sintoma_id):
        return self.sintomas.get(sintoma_id)

    def obtener_falla(self, falla_id):
        return self.fallas.get(falla_id)

    def obtener_recomendaciones(self, falla_id):
        return self.recomendaciones.get(falla_id, ["No hay recomendaciones disponibles para esta falla."])

    def obtener_fallas_por_sintoma(self, sintoma_id):
        ids_fallas = self.mapeo_sintomas_fallas.get(sintoma_id, [])
        return [self.fallas[fid] for fid in ids_fallas if fid in self.fallas]

    def obtener_todos_sintomas(self):
        return [{"id": k, **v} for k, v in self.sintomas.items()]

    def obtener_todas_fallas(self):
        return [{"id": k, **v} for k, v in self.fallas.items()]
