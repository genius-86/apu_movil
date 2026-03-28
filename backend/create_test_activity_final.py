
import os
import django
import sys
from datetime import datetime

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apu_backend.settings')
django.setup()

from core.models import Tercero, Actividad, Municipio, Barrio, TipoActividad, EstadoActividad
from django.utils import timezone

def create_activities():
    try:
        # 1. Get all active technicians
        tecnicos = Tercero.objects.filter(ejecuta_labor_tecnica='S', estado='A')
        if not tecnicos.exists():
            print("Error: No se encontraron técnicos activos.")
            return

        # 2. Get a municipio and barrio
        municipio = Municipio.objects.first()
        barrio = Barrio.objects.filter(id_municipio=municipio).first()
        
        # 3. Get activity type and state
        tipo = TipoActividad.objects.filter(descripcion__icontains='mantenimiento').first() or TipoActividad.objects.first()
        estado = EstadoActividad.objects.filter(descripcion__icontains='pendiente').first() or EstadoActividad.objects.get(id_estado_actividad=1)

        for tecnico in tecnicos:
            # 4. Create Activity for each technician
            actividad = Actividad.objects.create(
                id_tercero=tecnico,
                id_municipio=municipio,
                id_barrio=barrio,
                direccion=f"Calle de Prueba - {tecnico.nombre}",
                barrio=barrio.descripcion if barrio else "Barrio Central",
                fch_actividad=timezone.now(),
                id_tipo_actividad=tipo,
                id_estado_actividad=estado,
                observacion=f"PRUEBA PARA {tecnico.nombre}",
                latitud=0,
                longitud=0,
                fch_registro=timezone.now()
            )
            print(f"ÉXITO: Actividad #{actividad.id_actividad} creada para tecnico '{tecnico.nombre}' (ID: {tecnico.id_tercero})")

    except Exception as e:
        print(f"Error creando actividades: {str(e)}")

if __name__ == "__main__":
    create_activities()
