import json
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from diagnosticos.models import Regla


class Command(BaseCommand):
    help = 'Carga las reglas de produccion desde reglas.json a la base de datos'

    def handle(self, *args, **options):
        ruta_json = Path(__file__).resolve().parent.parent.parent.parent / 'conocimiento' / 'reglas.json'
        if not ruta_json.exists():
            self.stdout.write(self.style.ERROR(f"Archivo no encontrado: {ruta_json}"))
            return

        with open(ruta_json, 'r', encoding='utf-8') as f:
            reglas = json.load(f)

        for regla_data in reglas:
            obj, created = Regla.objects.update_or_create(
                codigo=regla_data['id'],
                defaults={
                    'nombre': regla_data['nombre'],
                    'categoria': regla_data['categoria'],
                    'condiciones': regla_data['condiciones'],
                    'conclusion': regla_data['conclusion'],
                    'acciones': regla_data['acciones'],
                    'explicacion': regla_data.get('explicacion', ''),
                    'prioridad': regla_data.get('prioridad', 10),
                    'activa': regla_data.get('activa', True),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Regla creada: {regla_data['id']}"))
            else:
                self.stdout.write(f"Regla actualizada: {regla_data['id']}")

        self.stdout.write(self.style.SUCCESS(f"Total: {len(reglas)} reglas procesadas"))
