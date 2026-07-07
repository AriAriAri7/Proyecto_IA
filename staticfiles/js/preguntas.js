var PreguntasManager = {
    currentQuestion: null,
    historialRespuestas: [],
    diagnosticoId: null,

    init: function(diagnosticoId) {
        this.diagnosticoId = diagnosticoId;
        this.historialRespuestas = [];
    },

    seleccionarSintoma: function(sintomaId) {
        document.getElementById('sintoma-seleccionado').value = sintomaId;
        document.getElementById('form-sintoma').submit();
    },

    responder: function(preguntaId, valor) {
        var card = document.getElementById('pregunta-card');
        if (!card) return;

        card.classList.add('animate-shake');
        setTimeout(function() {
            card.classList.remove('animate-shake');
        }, 600);

        var btns = document.querySelectorAll('.opcion-btn');
        btns.forEach(function(b) {
            b.disabled = true;
            if (b.dataset.valor === valor.toString().toLowerCase()) {
                b.className = 'btn btn-unefa opcion-btn w-100 text-start mb-2 selected';
            }
        });

        this.agregarHistorial(preguntaId, valor);

        var self = this;
        setTimeout(function() {
            self.enviarRespuesta(preguntaId, valor);
        }, 500);
    },

    enviarRespuesta: function(preguntaId, valor) {
        var data = {
            pregunta_id: preguntaId,
            respuesta: valor,
            diagnostico_id: this.diagnosticoId
        };

        fetch('/api/procesar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(data)
        })
        .then(function(response) {
            if (!response.ok) throw new Error('Error en la respuesta del servidor');
            return response.json();
        })
        .then(function(data) {
            if (data.completo) {
                window.location.href = data.redirect_url || ('/resultado/' + data.diagnostico_id + '/');
            } else if (data.pregunta) {
                PreguntasManager.mostrarSiguientePregunta(data);
            } else {
                showToast('Error al obtener la siguiente pregunta', 'error');
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            showToast('Error al procesar la respuesta. Intente de nuevo.', 'error');
            var btns2 = document.querySelectorAll('.opcion-btn');
            btns2.forEach(function(b) { b.disabled = false; });
        });
    },

    mostrarSiguientePregunta: function(data) {
        var card = document.getElementById('pregunta-card');
        var pregunta = data.pregunta;

        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';

        setTimeout(function() {
            var headerHtml = '<div class="pregunta-header mb-3">' +
                '<small class="text-muted">Pregunta ' + data.pregunta_numero + ' de ' + data.total_preguntas + '</small>' +
                '<span class="badge bg-info ms-2">' + (pregunta.categoria || 'General') + '</span>' +
                '</div>';

            var opcionesHtml = '';
            (pregunta.opciones || []).forEach(function(opcion) {
                var valor = typeof opcion.valor === 'boolean' ? opcion.valor.toString() : opcion.valor;
                opcionesHtml += '<button class="btn btn-outline-unefa opcion-btn w-100 text-start mb-2" ' +
                    'data-valor="' + valor.toLowerCase() + '" ' +
                    'data-pregunta-id="' + pregunta.id + '" ' +
                    'onclick="PreguntasManager.responder(\'' + pregunta.id + '\', \'' + valor.toLowerCase() + '\')">' +
                    '<i class="fas fa-circle-notch me-2"></i> ' + opcion.etiqueta +
                    '</button>';
            });

            card.querySelector('.card-body').innerHTML = headerHtml +
                '<h4 class="pregunta-texto mb-4"><i class="fas fa-question-circle text-primary me-2"></i>' + pregunta.pregunta + '</h4>' +
                '<div class="opciones-container">' + opcionesHtml + '</div>';

            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
            card.style.transition = 'all 0.4s ease';

            var progressBar = document.querySelector('.progress-bar');
            if (progressBar) {
                progressBar.style.width = data.progreso + '%';
                progressBar.textContent = data.progreso + '%';
                progressBar.setAttribute('aria-valuenow', data.progreso);
            }

            var progresoText = document.querySelector('.progress-bar-container .d-flex span:last-child');
            if (progresoText) {
                progresoText.textContent = data.pregunta_numero + ' de ' + data.total_preguntas;
            }
        }, 400);
    },

    agregarHistorial: function(preguntaId, valor) {
        var body = document.getElementById('historial-body');
        if (!body) return;

        var pregunta = this.obtenerTextoPregunta(preguntaId);
        var valorTexto = this.obtenerTextoRespuesta(preguntaId, valor);

        if (body.querySelector('.text-muted')) {
            body.innerHTML = '';
        }

        var item = document.createElement('div');
        item.className = 'historial-item mb-2 animate-slide-left';
        item.style.cssText = 'padding:8px 12px;background:var(--unefa-bg);border-radius:8px;border-left:3px solid var(--unefa-primary);';
        item.innerHTML = '<small class="text-muted">' + pregunta + '</small><br>' +
            '<strong><i class="fas fa-check-circle text-success"></i> ' + valorTexto + '</strong>';

        body.appendChild(item);
        body.scrollTop = body.scrollHeight;
    },

    obtenerTextoPregunta: function(preguntaId) {
        try {
            var preguntas = window.PREGUNTAS_DATA || [];
            var p = preguntas.find(function(q) { return q.id === preguntaId; });
            return p ? p.pregunta : 'Pregunta';
        } catch(e) {
            return 'Pregunta';
        }
    },

    obtenerTextoRespuesta: function(preguntaId, valor) {
        try {
            var preguntas = window.PREGUNTAS_DATA || [];
            var p = preguntas.find(function(q) { return q.id === preguntaId; });
            if (p) {
                var opcion = p.opciones.find(function(o) {
                    var ov = typeof o.valor === 'boolean' ? o.valor.toString().toLowerCase() : String(o.valor).toLowerCase();
                    return ov === valor.toLowerCase();
                });
                return opcion ? opcion.etiqueta : valor;
            }
        } catch(e) {}
        return valor;
    }
};

function responderPregunta(preguntaId, valor) {
    PreguntasManager.responder(preguntaId, valor);
}

function seleccionarSintoma(sintomaId) {
    PreguntasManager.seleccionarSintoma(sintomaId);
}
