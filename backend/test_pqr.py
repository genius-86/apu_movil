"""
Script de prueba para crear PQR y ver el error exacto
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apu_backend.settings')
django.setup()

from core.models import Pqr, Municipio, TipoPqr, TipoReporte, MedioRecepcionPqr, EstadoPqr, Tercero
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
    'fch_registro': datetime.now()
}

try:
    # Verificar que existan las foreign keys
    print("Verificando foreign keys...")
    municipio = Municipio.objects.get(id_municipio=data['id_municipio'])
    print(f"✓ Municipio: {municipio}")
    
    tipo_pqr = TipoPqr.objects.get(id_tipo_pqr=data['id_tipo_pqr'])
    print(f"✓ Tipo PQR: {tipo_pqr}")
    
    tipo_reporte = TipoReporte.objects.get(id_tipo_reporte=data['id_tipo_reporte'])
    print(f"✓ Tipo Reporte: {tipo_reporte}")
    
    medio = MedioRecepcionPqr.objects.get(id_medio_recepcion_pqr=data['id_medio_recepcion_pqr'])
    print(f"✓ Medio Recepción: {medio}")
    
    estado = EstadoPqr.objects.get(id_estado_pqr=data['id_estado_pqr'])
    print(f"✓ Estado: {estado}")
    
    tercero = Tercero.objects.get(id_tercero=data['id_tercero_registra'])
    print(f"✓ Tercero: {tercero}")
    
    # Intentar crear PQR
    print("\nCreando PQR...")
    pqr = Pqr.objects.create(**data)
    print(f"✓ PQR creada exitosamente: {pqr.id_pqr}")
    
except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    import traceback
    traceback.print_exc()
