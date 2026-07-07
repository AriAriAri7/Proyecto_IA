document.addEventListener('DOMContentLoaded', function() {
    if (typeof DIAGNOSTICO_ID !== 'undefined' && DIAGNOSTICO_ID) {
        PreguntasManager.init(DIAGNOSTICO_ID);
        cargarPreguntasData();
    }

    initDiagnosticoRapido();
    initFiltroHistorial();
});

function cargarPreguntasData() {
    fetch('/api/preguntas/')
        .then(function(response) { return response.json(); })
        .then(function(data) {
            window.PREGUNTAS_DATA = data.preguntas || [];
        })
        .catch(function(err) {
            console.warn('No se pudieron cargar las preguntas:', err);
        });
}

function initDiagnosticoRapido() {
    var form = document.getElementById('form-diagnostico-rapido');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(form);
        var sintomas = {};

        formData.forEach(function(value, key) {
            sintomas[key] = value === 'true' || value === true;
        });

        if (Object.keys(sintomas).length === 0) {
            showToast('Selecciona al menos un sintoma', 'warning');
            return;
        }

        var btn = form.querySelector('button[type="submit"]');
        btn.disabled = true;
        btn.innerHTML = '<span class="loading-spinner"></span> Diagnosticando...';

        fetch('/api/diagnosticar-rapido/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ sintomas: sintomas })
        })
        .then(function(response) {
            if (!response.ok) throw new Error('Error en el diagnostico');
            return response.json();
        })
        .then(function(data) {
            if (data.success && data.resultado) {
                showToast('Diagnostico completado con exito', 'success');
                window.location.href = '/resultado/' + data.diagnostico_id + '/';
            } else {
                showToast('Error al obtener el resultado', 'error');
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-search"></i> Diagnosticar';
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            showToast('Error al realizar el diagnostico rapido', 'error');
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-search"></i> Diagnosticar';
        });
    });
}

function initFiltroHistorial() {
    var searchInput = document.getElementById('search-historial');
    if (!searchInput) return;

    var debounceTimer;
    searchInput.addEventListener('keyup', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            var value = searchInput.value.toLowerCase();
            var rows = document.querySelectorAll('#tabla-historial tbody tr');
            rows.forEach(function(row) {
                var text = row.textContent.toLowerCase();
                row.style.display = text.includes(value) ? '' : 'none';
            });
        }, 300);
    });
}

function exportarResultado(diagnosticoId) {
    window.open('/resultado/' + diagnosticoId + '/?export=pdf', '_blank');
}

function compartirResultado(diagnosticoId) {
    var url = window.location.origin + '/resultado/' + diagnosticoId + '/';
    if (navigator.share) {
        navigator.share({
            title: 'Resultado de Diagnostico',
            text: 'Resultado del diagnostico de fallas del equipo',
            url: url
        }).catch(function(err) {
            console.log('Error al compartir:', err);
        });
    } else {
        navigator.clipboard.writeText(url).then(function() {
            showToast('Enlace copiado al portapapeles', 'success');
        });
    }
}

function mostrarDetalleRegla(reglaId) {
    var modal = new bootstrap.Modal(document.getElementById('modal-regla-detalle'));
    document.getElementById('modal-regla-contenido').innerHTML = '<div class="text-center"><div class="loading-spinner"></div><p class="mt-2">Cargando...</p></div>';
    modal.show();

    fetch('/api/regla-detalle/?regla_id=' + reglaId)
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.error) {
                document.getElementById('modal-regla-contenido').innerHTML = '<p class="text-danger">' + data.error + '</p>';
                return;
            }
            document.getElementById('modal-regla-contenido').innerHTML = '' +
                '<h5>' + data.id + ' - ' + data.nombre + '</h5>' +
                '<p><strong>Categoria:</strong> ' + data.categoria + '</p>' +
                '<p><strong>Condiciones:</strong></p><ul>' +
                Object.keys(data.condiciones).map(function(k) { return '<li><code>' + k + ' = ' + data.condiciones[k] + '</code></li>'; }).join('') +
                '</ul>' +
                '<p><strong>Conclusion:</strong> <code>' + data.conclusion + '</code></p>' +
                '<p><strong>Prioridad:</strong> ' + data.prioridad + '</p>' +
                (data.explicacion ? '<p><strong>Explicacion:</strong> ' + data.explicacion + '</p>' : '');
        })
        .catch(function(err) {
            document.getElementById('modal-regla-contenido').innerHTML = '<p class="text-danger">Error al cargar los detalles</p>';
        });
}

function reiniciarDiagnostico() {
    if (confirm('Esta accion reiniciara el diagnostico actual. Desea continuar?')) {
        fetch('/api/nuevo-diagnostico/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({})
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.success) {
                window.location.href = '/diagnostico/' + data.diagnostico_id + '/';
            }
        })
        .catch(function(err) {
            showToast('Error al reiniciar el diagnostico', 'error');
        });
    }
}
