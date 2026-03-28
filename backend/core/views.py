from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import (
    Tercero, Actividad, Luminaria, TipoActividad, Municipio, Barrio, Pqr,
    TipoPqr, TipoReporte, MedioRecepcionPqr, EstadoPqr,
    Articulo, ActividadMaterial, ActividadFoto, ActividadFirma, ActividadMobile,
    EstadoActividad, UnidadMedida, Vehiculo
)
from .serializers import (
    TerceroSerializer, ActividadSerializer, LuminariaSerializer, 
    TipoActividadSerializer, MunicipioSerializer, BarrioSerializer,
    PqrSerializer, TipoPqrSerializer, TipoReporteSerializer, 
    MedioRecepcionPqrSerializer, EstadoPqrSerializer,
    ArticuloSerializer, ActividadMaterialSerializer, ActividadFotoSerializer, ActividadFirmaSerializer,
    EstadoActividadSerializer, UnidadMedidaSerializer, VehiculoSerializer
)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly]) # Or IsAuthenticated depending on previous decision (we removed global IsAuthenticated)
def api_root(request, format=None):
    return Response({
        'Módulo Operativo': {
            'Actividades': reverse('actividad-list', request=request, format=format),
            'Luminarias': reverse('luminaria-list', request=request, format=format),
            # 'Reportes PQR': reverse('pqr-list', request=request, format=format), # Add when PQR ViewSet exists
        },
        'Módulo Administrativo': {
            'Usuarios (Terceros)': reverse('tercero-list', request=request, format=format),
            'Municipios': reverse('municipio-list', request=request, format=format),
            'Barrios': reverse('barrio-list', request=request, format=format),
        },
        'Configuración': {
            'Tipos de Actividad': reverse('tipoactividad-list', request=request, format=format),
        }
    })

from .permissions import IsAdminUserCustom

class TerceroViewSet(viewsets.ModelViewSet):
    queryset = Tercero.objects.all()
    serializer_class = TerceroSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserCustom]

class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all().order_by('-fch_actividad')
    serializer_class = ActividadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['id_tercero', 'id_municipio', 'id_tipo_actividad', 'id_estado_actividad']
    search_fields = ['direccion', 'observacion', 'id_luminaria__poste_no']

    def get_queryset(self):
        queryset = super().get_queryset()
        # If user is a technician, show only their activities
        if not self.request.user.super_usuario == 'S':
            queryset = queryset.filter(id_tercero=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(id_tercero_registra=self.request.user)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """
        Marca la hora de inicio y posición geográfica en tabla auxiliar.
        """
        actividad = self.get_object()
        from django.utils import timezone
        
        latitud = request.data.get('latitud')
        longitud = request.data.get('longitud')
        
        # Create or update mobile detail
        mobile_data, created = ActividadMobile.objects.get_or_create(id_actividad=actividad)
        mobile_data.fch_inicio = timezone.now()
        if latitud is not None: mobile_data.latitud_inicio = latitud
        if longitud is not None: mobile_data.longitud_inicio = longitud
        mobile_data.save()
        
        return Response({
            'status': 'Actividad iniciada',
            'fch_inicio': mobile_data.fch_inicio,
            'posicion': {'lat': latitud, 'lng': longitud}
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_material(self, request, pk=None):
        actividad = self.get_object()
        serializer = ActividadMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id_actividad=actividad)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_photo(self, request, pk=None):
        actividad = self.get_object()
        serializer = ActividadFotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id_actividad=actividad)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_signature(self, request, pk=None):
        actividad = self.get_object()
        serializer = ActividadFirmaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id_actividad=actividad)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def finish(self, request, pk=None):
        actividad = self.get_object()
        
        # 1. Close associated PQR if exists
        if actividad.id_pqr:
            pqr = actividad.id_pqr
            closed_status = EstadoPqr.objects.filter(descripcion__icontains='cerrado').first()
            if closed_status:
                pqr.id_estado_pqr = closed_status
                from django.utils import timezone
                pqr.fch_cierre = timezone.now()
                pqr.save()
        
        return Response({'status': 'Actividad finalizada'}, status=status.HTTP_200_OK)

class ArticuloViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['clase']
    search_fields = ['descripcion']

class ActividadMaterialViewSet(viewsets.ModelViewSet):
    queryset = ActividadMaterial.objects.all()
    serializer_class = ActividadMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActividadFotoViewSet(viewsets.ModelViewSet):
    queryset = ActividadFoto.objects.all()
    serializer_class = ActividadFotoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActividadFirmaViewSet(viewsets.ModelViewSet):
    queryset = ActividadFirma.objects.all()
    serializer_class = ActividadFirmaSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_form_parameters(request):
    """
    Lista parámetros de algunos data-list utilizados para diligenciar el formulario.
    """
    return Response({
        'municipios': MunicipioSerializer(Municipio.objects.all(), many=True).data,
        'barrios': BarrioSerializer(Barrio.objects.all(), many=True).data,
        'tipos_actividad': TipoActividadSerializer(TipoActividad.objects.all(), many=True).data,
        'articulos': ArticuloSerializer(Articulo.objects.all(), many=True).data,
        'estados_actividad': EstadoActividadSerializer(EstadoActividad.objects.all(), many=True).data,
        'vehiculos': VehiculoSerializer(Vehiculo.objects.filter(estado='A'), many=True).data,
        'unidades_medida': UnidadMedidaSerializer(UnidadMedida.objects.all(), many=True).data,
        'tipos_pqr': TipoPqrSerializer(TipoPqr.objects.filter(estado='A'), many=True).data,
        'tipos_reporte': TipoReporteSerializer(TipoReporte.objects.all(), many=True).data,
    })

class LuminariaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Luminaria.objects.all()
    serializer_class = LuminariaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['poste_no', 'luminaria_no', 'id_municipio', 'id_barrio']
    search_fields = ['poste_no', 'luminaria_no', 'direccion', 'referencia']

class TipoActividadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoActividad.objects.all()
    serializer_class = TipoActividadSerializer
    permission_classes = [permissions.IsAuthenticated]

class MunicipioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    permission_classes = [permissions.IsAuthenticated]

class BarrioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Barrio.objects.all()
    serializer_class = BarrioSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vistas para Módulo PQR

class TipoPqrViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoPqr.objects.all()
    serializer_class = TipoPqrSerializer
    permission_classes = [permissions.IsAuthenticated]

class TipoReporteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoReporte.objects.all()
    serializer_class = TipoReporteSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedioRecepcionPqrViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MedioRecepcionPqr.objects.all()
    serializer_class = MedioRecepcionPqrSerializer
    permission_classes = [permissions.IsAuthenticated]

class EstadoPqrViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EstadoPqr.objects.all()
    serializer_class = EstadoPqrSerializer
    permission_classes = [permissions.IsAuthenticated]

class PqrViewSet(viewsets.ModelViewSet):
    queryset = Pqr.objects.all().order_by('-fch_registro')
    serializer_class = PqrSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['id_municipio', 'id_estado_pqr', 'id_tipo_pqr']

    def asignar_tecnico(self, municipio, tipo_reporte=None):
        """
        Asigna un técnico basado en el municipio y carga de trabajo.
        Retorna el técnico con menos actividades pendientes en ese municipio.
        """
        from django.db.models import Count, Q
        
        # Obtener técnicos que ejecutan labor técnica en el municipio
        tecnicos = Tercero.objects.filter(
            ejecuta_labor_tecnica='S',
            id_municipio=municipio
        )
        
        if not tecnicos.exists():
            # Si no hay técnicos en ese municipio, buscar en cualquier municipio
            tecnicos = Tercero.objects.filter(ejecuta_labor_tecnica='S')
        
        if not tecnicos.exists():
            return None
        
        # Contar actividades pendientes (estados 1 y 2 típicamente son pendiente/en proceso)
        # Ajustar según los IDs reales de tu base de datos
        tecnico_asignado = tecnicos.annotate(
            actividades_pendientes=Count(
                'actividad',
                filter=Q(actividad__id_estado_actividad__in=[1, 2])
            )
        ).order_by('actividades_pendientes').first()
        
        return tecnico_asignado

    def create(self, request, *args, **kwargs):
        """
        Override create to:
        1. Create PQR
        2. Automatically assign technician
        3. Create associated Activity
        """
        import logging
        from django.utils import timezone
        logger = logging.getLogger(__name__)
        
        logger.info(f"PQR Create - Received data: {request.data}")
        
        # Validar y crear PQR
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"PQR Validation errors: {serializer.errors}")
            return Response({
                'error': 'Validation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Guardar PQR
        pqr = serializer.save()
        logger.info(f"PQR created: {pqr.id_pqr}")
        
        # Asignar técnico
        tecnico = self.asignar_tecnico(
            municipio=pqr.id_municipio,
            tipo_reporte=pqr.id_tipo_reporte
        )
        
        if tecnico:
            logger.info(f"Técnico asignado: {tecnico.nombre} {tecnico.apellido}")
            
            # Crear actividad automáticamente
            try:
                # Obtener estado inicial de actividad (típicamente "Pendiente" o similar)
                # Ajustar según tu base de datos
                estado_inicial = TipoActividad.objects.filter(
                    descripcion__icontains='pendiente'
                ).first() or TipoActividad.objects.first()
                
                actividad = Actividad.objects.create(
                    id_pqr=pqr,
                    id_tercero=tecnico,
                    id_tipo_reporte=pqr.id_tipo_reporte,
                    id_municipio=pqr.id_municipio,
                    id_luminaria=pqr.id_luminaria,
                    id_tipo_actividad=estado_inicial,
                    id_estado_actividad=estado_inicial.id_tipo_actividad if estado_inicial else 1,
                    direccion=pqr.direccion_reporte or 'Sin dirección',
                    fch_actividad=timezone.now(),
                    fch_reporte=pqr.fch_pqr,
                    observacion=f"Actividad generada automáticamente desde PQR #{pqr.id_pqr}",
                    latitud=0,  # Se actualizará cuando el técnico inicie
                    longitud=0,
                    id_tercero_registra=request.user if hasattr(request.user, 'id_tercero') else pqr.id_tercero_registra,
                    fch_registro=timezone.now()
                )
                
                logger.info(f"Actividad creada: {actividad.id_actividad}")
                
            except Exception as e:
                logger.error(f"Error creating activity: {str(e)}")
                # No fallar la creación de PQR si falla la actividad
        else:
            logger.warning("No se pudo asignar técnico - no hay técnicos disponibles")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


