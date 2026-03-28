from rest_framework import serializers
from .models import (
    Tercero, Actividad, Luminaria, Pqr, TipoActividad, Municipio, Barrio, 
    TipoLuminaria, EstadoLuminaria, TipoPqr, TipoReporte, MedioRecepcionPqr, EstadoPqr,
    Articulo, ActividadMaterial, ActividadFoto, ActividadFirma, ActividadMobile,
    EstadoActividad, UnidadMedida, Vehiculo
)

import hashlib

class TerceroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Tercero
        fields = ['id_tercero', 'nombre', 'apellido', 'usuario', 'email', 'es_usuario', 'super_usuario', 'ejecuta_labor_tecnica', 'password', 'identificacion', 'direccion', 'telefono', 'estado']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = Tercero(**validated_data)
        if password:
            instance.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        instance.save()
        return instance

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

class BarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrio
        fields = '__all__'

class TipoLuminariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoLuminaria
        fields = '__all__'

class LuminariaSerializer(serializers.ModelSerializer):
    tipo_luminaria_desc = serializers.ReadOnlyField(source='id_tipo_luminaria.descripcion')
    estado_desc = serializers.ReadOnlyField(source='id_estado_luminaria.descripcion')
    barrio_desc = serializers.ReadOnlyField(source='id_barrio.descripcion')
    municipio_desc = serializers.ReadOnlyField(source='id_municipio.descripcion')

    class Meta:
        model = Luminaria
        fields = '__all__'

class TipoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoActividad
        fields = '__all__'

class EstadoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoActividad
        fields = '__all__'

class UnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = '__all__'

class ActividadMaterialSerializer(serializers.ModelSerializer):
    articulo_desc = serializers.ReadOnlyField(source='id_articulo.descripcion')
    unidad_medida_desc = serializers.ReadOnlyField(source='id_unidad_medida.abreviatura')
    
    class Meta:
        model = ActividadMaterial
        fields = '__all__'

class ActividadFotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadFoto
        fields = '__all__'

class ActividadFirmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadFirma
        fields = '__all__'

class ActividadMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadMobile
        fields = '__all__'

class ActividadSerializer(serializers.ModelSerializer):
    tipo_actividad_desc = serializers.ReadOnlyField(source='id_tipo_actividad.descripcion')
    estado_actividad_desc = serializers.ReadOnlyField(source='id_estado_actividad.descripcion')
    vehiculo_desc = serializers.ReadOnlyField(source='id_vehiculo.placa')
    materiales = ActividadMaterialSerializer(many=True, required=False)
    fotos = ActividadFotoSerializer(many=True, read_only=True)
    firma = ActividadFirmaSerializer(read_only=True)
    mobile_data = ActividadMobileSerializer(read_only=True)
    
    # Extra fields for logic
    cerrar_pqr = serializers.BooleanField(write_only=True, required=False, default=False)
    firma_tecnico = serializers.CharField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Actividad
        fields = '__all__'

    def update(self, instance, validated_data):
        materiales_data = validated_data.pop('materiales', None)
        cerrar_pqr = validated_data.pop('cerrar_pqr', False)
        firma_tecnico = validated_data.pop('firma_tecnico', None)
        
        # Actualizar campos de la actividad
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Legacy parity: if fch_ejecucion_actividad is updated, set fch_reporte
        if 'fch_ejecucion_actividad' in validated_data:
            from django.utils import timezone
            instance.fch_reporte = timezone.now()

        instance.save()

        # Manejar materiales (Sobre-escritura simple)
        if materiales_data is not None:
            instance.materiales.all().delete()
            for mat_data in materiales_data:
                # Remove read-only or extra fields if present from frontend
                mat_data.pop('articulo_desc', None)
                ActividadMaterial.objects.create(id_actividad=instance, **mat_data)

        # Manejar firma técnica
        if firma_tecnico:
            # Upsert de la firma
            from .models import ActividadFirma
            firma_obj, created = ActividadFirma.objects.get_or_create(id_actividad=instance)
            # Use assigned technician name or fallback
            nombre = "Técnico"
            if instance.id_tercero:
                nombre = f"{instance.id_tercero.nombre or ''} {instance.id_tercero.apellido or ''}".strip()
            
            firma_obj.nombre_firmante = nombre or "Técnico Responsable"
            firma_obj.firma_base64 = firma_tecnico
            firma_obj.save()

        # Cerrar PQR si aplica
        if cerrar_pqr and instance.id_pqr:
            pqr = instance.id_pqr
            # Import models here to avoid circular dependencies if any
            from .models import EstadoPqr
            closed_status = EstadoPqr.objects.filter(descripcion__icontains='cerrado').first()
            if closed_status:
                pqr.id_estado_pqr = closed_status
                from django.utils import timezone
                pqr.fch_cierre = timezone.now()
                pqr.save()

        return instance

# Serializadores para Módulo PQR

class TipoPqrSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPqr
        fields = '__all__'

class TipoReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoReporte
        fields = '__all__'

class MedioRecepcionPqrSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedioRecepcionPqr
        fields = '__all__'

class EstadoPqrSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPqr
        fields = '__all__'

class PqrSerializer(serializers.ModelSerializer):
    # Read-only fields for display
    tipo_pqr_desc = serializers.ReadOnlyField(source='id_tipo_pqr.descripcion')
    tipo_reporte_desc = serializers.ReadOnlyField(source='id_tipo_reporte.descripcion')
    medio_recepcion_desc = serializers.ReadOnlyField(source='id_medio_recepcion_pqr.descripcion')
    estado_desc = serializers.ReadOnlyField(source='id_estado_pqr.descripcion')
    municipio_desc = serializers.ReadOnlyField(source='id_municipio.descripcion')
    nombre_tercero_registra = serializers.ReadOnlyField(source='id_tercero_registra.nombre')
    poste_no = serializers.ReadOnlyField(source='id_luminaria.poste_no')
    tipo_luminaria_desc = serializers.ReadOnlyField(source='id_luminaria.id_tipo_luminaria.descripcion')
    
    # Información del técnico asignado (desde la actividad asociada)
    tecnico_asignado = serializers.SerializerMethodField()
    estado_actividad = serializers.SerializerMethodField()
    
    # Explicitly define ForeignKey fields to accept IDs
    id_municipio = serializers.PrimaryKeyRelatedField(queryset=Municipio.objects.all())
    id_tipo_pqr = serializers.PrimaryKeyRelatedField(queryset=TipoPqr.objects.all())
    id_tipo_reporte = serializers.PrimaryKeyRelatedField(queryset=TipoReporte.objects.all())
    id_medio_recepcion_pqr = serializers.PrimaryKeyRelatedField(queryset=MedioRecepcionPqr.objects.all())
    id_estado_pqr = serializers.PrimaryKeyRelatedField(queryset=EstadoPqr.objects.all())
    id_tercero_registra = serializers.PrimaryKeyRelatedField(queryset=Tercero.objects.all())
    id_luminaria = serializers.PrimaryKeyRelatedField(queryset=Luminaria.objects.all(), required=False, allow_null=True)
    id_tercero_cierra = serializers.PrimaryKeyRelatedField(queryset=Tercero.objects.all(), required=False, allow_null=True)
    
    def get_tecnico_asignado(self, obj):
        """Obtiene el técnico asignado desde la actividad asociada"""
        try:
            actividad = obj.actividad_set.first()
            if actividad and actividad.id_tercero:
                return {
                    'id': actividad.id_tercero.id_tercero,
                    'nombre': f"{actividad.id_tercero.nombre} {actividad.id_tercero.apellido}"
                }
        except:
            pass
        return None
    
    def get_estado_actividad(self, obj):
        """Obtiene el estado de la actividad asociada"""
        try:
            actividad = obj.actividad_set.first()
            if actividad:
                return {
                    'id_actividad': actividad.id_actividad,
                    'estado': 'Pendiente'  # Ajustar según tu lógica
                }
        except:
            pass
        return None
    
    class Meta:
        model = Pqr
        fields = '__all__'

