from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def json_parse(value):
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}


@register.filter
def json_dumps(value):
    try:
        return json.dumps(value, ensure_ascii=False, indent=2)
    except (TypeError, ValueError):
        return str(value)


@register.simple_tag
def gravedad_badge(gravedad):
    colores = {'critico': 'danger', 'medio': 'warning', 'bajo': 'info'}
    color = colores.get(gravedad, 'secondary')
    return mark_safe(f'<span class="badge bg-{color}">{gravedad|upper}</span>')


@register.simple_tag
def estado_badge(estado):
    colores = {'en_curso': 'primary', 'completado': 'success', 'cancelado': 'secondary'}
    color = colores.get(estado, 'dark')
    return mark_safe(f'<span class="badge bg-{color}">{estado}</span>')


@register.filter
def porcentaje_a_color(value):
    if value >= 80:
        return '#28a745'
    elif value >= 50:
        return '#ffc107'
    else:
        return '#dc3545'
