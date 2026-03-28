
import os
import django
import sys
import json

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apu_backend.settings')
django.setup()

from core.models import Actividad, Vehiculo, EstadoActividad
from core.serializers import ActividadSerializer, VehiculoSerializer

def debug_parameters():
    try:
        # Check active vehicles
        vehiculos = Vehiculo.objects.filter(estado='A')
        print(f"Vehículos activos: {vehiculos.count()}")
        for v in vehiculos:
            print(f"- ID: {v.id_vehiculo}, Placa: {v.placa}, Desc: {v.descripcion}")

        # Check last activity
        act = Actividad.objects.order_by('-id_actividad').first()
        if act:
            print(f"\nÚltima Actividad ID: {act.id_actividad}")
            print(f"Estado Actividad: {act.id_estado_actividad.descripcion} (ID: {act.id_estado_actividad.id_estado_actividad})")
            print(f"Vehículo actual: {act.id_vehiculo_id} ({act.id_vehiculo.placa if act.id_vehiculo else 'Ninguno'})")
            
            serializer = ActividadSerializer(act)
            print("\nSerializado (lo que recibe el frontend):")
            # Convert to dict and print
            data = serializer.data
            print(json.dumps(data, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    debug_parameters()
