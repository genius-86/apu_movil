
import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apu_backend.settings')
django.setup()

from core.models import EstadoActividad

def check_states():
    try:
        states = EstadoActividad.objects.all()
        print("ESTADOS DE ACTIVIDAD ENCONTRADOS:")
        for s in states:
            print(f"ID: {s.id_estado_actividad} | Descripcion: {s.descripcion}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_states()
