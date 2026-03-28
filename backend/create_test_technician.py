
import os
import django
import hashlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apu_backend.settings')
django.setup()

from core.models import Tercero, TipoIdentificacion, Municipio

def create_technician():
    username = 'tecnico_prueba'
    password = 'password123'
    md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()

    # Check if exists
    if Tercero.objects.filter(usuario=username).exists():
        print(f"El usuario '{username}' ya existe.")
        return

    # Get dependencies (assuming they exist, otherwise use defaults or create)
    # Buscamos un tipo de identificacion y municipio cualquiera para llenar FKs
    tipo_id = TipoIdentificacion.objects.first()
    municipio = Municipio.objects.first()

    if not tipo_id or not municipio:
        print("Error: Se requieren datos previos en TipoIdentificacion y Municipio.")
        return

    tecnico = Tercero(
        usuario=username,
        password=md5_password, # Campo 'clave' en DB
        nombre='Juan',
        apellido='Perez Tecnico',
        identificacion='123456789',
        email='tecnico@prueba.com',
        direccion='Calle Falsa 123',
        telefono='555-5555',
        ejecuta_labor_tecnica='S',
        es_empleado='S',
        es_usuario='S',
        estado='A',
        id_tipo_identificacion=tipo_id,
        id_municipio=municipio
    )
    tecnico.save()
    print(f"Usuario '{username}' creado exitosamente con contraseña '{password}'.")

if __name__ == '__main__':
    create_technician()
