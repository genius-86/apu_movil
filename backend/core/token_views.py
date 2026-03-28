from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add extra responses data
        data['user'] = {
            'id_tercero': self.user.id_tercero,
            'usuario': self.user.usuario,
            'nombre': self.user.nombre,
            'apellido': self.user.apellido,
            'email': self.user.email,
            'es_admin': self.user.super_usuario in ['S', '1', 's'],
            'es_tecnico': self.user.ejecuta_labor_tecnica in ['S', '1', 's']
        }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
