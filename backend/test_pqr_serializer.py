"""
Script de prueba para crear PQR usando el serializer
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apu_backend.settings')
django.setup()

from core.serializers import PqrSerializer
from datetime import datetime

# Datos de prueba (los mismos que envía el frontend)
data = {
    'id_municipio': 7,
    'id_tipo_pqr': 7,
    'id_tipo_reporte': 5,
    'id_medio_recepcion_pqr': 7,
    'id_estado_pqr': 1,
    'comentario': 'farola apagada',
    'direccion_reporte': 'calle 20 # 30-50',
    'nombre_usuario_servicio': 'carlos',
    'fch_pqr': '2026-01-28',
    'id_tercero_registra': 21,
    'fch_registro': datetime.now().isoformat()
}

try:
    print("Probando serializer con datos:", data)
    print()
    
    serializer = PqrSerializer(data=data)
    
    if serializer.is_valid():
        print("✓ Serializer válido!")
        pqr = serializer.save()
        print(f"✓ PQR creada exitosamente: ID {pqr.id_pqr}")
        print(f"  Municipio: {pqr.id_municipio}")
        print(f"  Tipo: {pqr.id_tipo_pqr}")
        print(f"  Estado: {pqr.id_estado_pqr}")
    else:
        print("✗ Errores de validación:")
        for field, errors in serializer.errors.items():
            print(f"  - {field}: {errors}")
    
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    import traceback
    traceback.print_exc()
