from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Actividad, Pqr, Luminaria, Tercero

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        
        # Determine Role
        is_admin = user.super_usuario == 'S' or user.super_usuario == '1'
        is_technician = user.ejecuta_labor_tecnica == 'S' or user.ejecuta_labor_tecnica == '1'
        
        stats = []

        if is_technician and not is_admin:
            # --- VIEW FOR TECHNICIAN ---
            # 1. Assigned Activities (Pending?)
            # Assuming 'id_tercero' in Actividad represents the assigned technician.
            # And we need a way to know if it's pending. Typically no execution date?
            # Looking at Actividad model, let's assume we filter by assigned to user.
            
            mis_actividades_total = Actividad.objects.filter(id_tercero=user.id_tercero).count()
            
            # This is a guess on "Pendientes" logic for legacy DB, usually null date or specific state.
            # Let's count Total assigned for now as "Asignadas"
            
            stats = [
                { 'label': 'Mis Actividades', 'value': str(mis_actividades_total), 'desc': 'Total Asignadas', 'icon': 'ClipboardList', 'color': 'text-blue-500', 'bg': 'bg-blue-500/10' },
                { 'label': 'Materiales', 'value': '0', 'desc': 'En custodia', 'icon': 'Box', 'color': 'text-orange-500', 'bg': 'bg-orange-500/10' }, # Placeholder for inventory
                { 'label': 'Eficacia', 'value': '100%', 'desc': 'Personal', 'icon': 'TrendingUp', 'color': 'text-green-500', 'bg': 'bg-green-500/10' },
            ]

        else:
            # --- VIEW FOR ADMIN/MANAGER (Default) ---
            
            # PQR Pendientes: fch_cierre IS NULL
            pqr_pendientes = Pqr.objects.filter(fch_cierre__isnull=True).count()
            
            # Actividades Total
            actividades_total = Actividad.objects.count()

            # Luminarias Total
            luminarias_total = Luminaria.objects.count()

            # Tecnicos Activos
            tecnicos_activos = Tercero.objects.filter(ejecuta_labor_tecnica='S', estado='A').count()

            stats = [
                { 'label': 'PQRs Pendientes', 'value': str(pqr_pendientes), 'desc': 'Sin cerrar', 'icon': 'Clock', 'color': 'text-orange-500', 'bg': 'bg-orange-500/10' },
                { 'label': 'Actividades', 'value': str(actividades_total), 'desc': 'Histórico Total', 'icon': 'CheckCircle', 'color': 'text-green-500', 'bg': 'bg-green-500/10' },
                { 'label': 'Luminarias', 'value': str(luminarias_total), 'desc': 'Inventario Red', 'icon': 'TrendingUp', 'color': 'text-purple-500', 'bg': 'bg-purple-500/10' },
                { 'label': 'Técnicos', 'value': str(tecnicos_activos), 'desc': 'Operativos', 'icon': 'Users', 'color': 'text-blue-500', 'bg': 'bg-blue-500/10' },
            ]
        
        return Response({
            'stats': stats,
            'role': 'Técnico' if (is_technician and not is_admin) else 'Administrador'
        })
