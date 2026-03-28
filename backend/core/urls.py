from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TerceroViewSet, ActividadViewSet, LuminariaViewSet, 
    TipoActividadViewSet, MunicipioViewSet, BarrioViewSet,
    PqrViewSet, TipoPqrViewSet, TipoReporteViewSet, 
    MedioRecepcionPqrViewSet, EstadoPqrViewSet,
    ArticuloViewSet, ActividadMaterialViewSet, ActividadFotoViewSet, ActividadFirmaViewSet,
    get_form_parameters, api_root
)

router = DefaultRouter()
router.register(r'terceros', TerceroViewSet)
router.register(r'actividades', ActividadViewSet)
router.register(r'luminarias', LuminariaViewSet)
router.register(r'tipos-actividad', TipoActividadViewSet)
router.register(r'municipios', MunicipioViewSet)
router.register(r'barrios', BarrioViewSet)
router.register(r'articulos', ArticuloViewSet)
router.register(r'actividad-materiales', ActividadMaterialViewSet)
router.register(r'actividad-fotos', ActividadFotoViewSet)
router.register(r'actividad-firmas', ActividadFirmaViewSet)

# Rutas PQR
router.register(r'pqr', PqrViewSet)
router.register(r'tipos-pqr', TipoPqrViewSet)
router.register(r'tipos-reporte', TipoReporteViewSet)
router.register(r'medios-recepcion', MedioRecepcionPqrViewSet)
router.register(r'estados-pqr', EstadoPqrViewSet)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('parametros/', get_form_parameters, name='form-parameters'),
    path('', include(router.urls)),
]
