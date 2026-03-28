import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apu_backend.settings')
django.setup()

from core.models import Tercero, Actividad, TipoActividad, Municipio, EstadoActividad

def create_pending_activity():
    # Find tecnico_prueba
    tecnico = Tercero.objects.filter(usuario='tecnico_prueba').first()
    if not tecnico:
        print("El técnico 'tecnico_prueba' no existe.")
        return

    # Find necessary dependencies
    municipio = Municipio.objects.first()
    if not municipio:
        print("Error: No hay municipios en la BD.")
        return

    tipo_actividad = TipoActividad.objects.filter(descripcion__icontains='pendiente').first()
    if not tipo_actividad:
        tipo_actividad = TipoActividad.objects.first()
        if not tipo_actividad:
            print("Error: No hay TipoActividad en la BD.")
            return

    estado_actividad = EstadoActividad.objects.first()
    if not estado_actividad:
        print("Error: No hay EstadoActividad en la BD.")
        return
        
    print(f"Creando actividad pendiente para el técnico {tecnico.nombre}...")
    actividad = Actividad(
        id_tercero=tecnico,
        id_municipio=municipio,
        id_tipo_actividad=tipo_actividad,
        id_estado_actividad=estado_actividad,
        direccion='Calle Falsa Test 123',
        fch_actividad=timezone.now(),
        fch_registro=timezone.now(),
        observacion='Actividad de prueba generada automáticamente',
        latitud=0,
        longitud=0,
        id_tercero_registra=tecnico  # Para simplificar
    )
    actividad.save()
    print(f"¡Actividad {actividad.id_actividad} creada exitosamente!")

if __name__ == '__main__':
    create_pending_activity()
