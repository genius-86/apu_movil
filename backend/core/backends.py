import hashlib
from django.contrib.auth.backends import BaseBackend
from .models import Tercero

class LegacyMySQLBackend(BaseBackend):
    def authenticate(self, request, usuario=None, password=None, **kwargs):
        print(f"DEBUG AUTH: usuario={usuario}, password={password}, kwargs={kwargs}")
        if usuario is None:
            usuario = kwargs.get('username')
            print(f"DEBUG AUTH: Retrieved username from kwargs: {usuario}")
            
        if not usuario or not password:
            print("DEBUG AUTH: Missing credentials")
            return None
        
        try:
            user = Tercero.objects.get(usuario=usuario)
            print(f"DEBUG AUTH: User found: {user}")
        except Tercero.DoesNotExist:
            print("DEBUG AUTH: User does not exist")
            return None

        # Calculate MD5 of the input password
        input_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        print(f"DEBUG AUTH: Input hash: {input_hash}, Stored: {user.password}")
        
        if user.password == input_hash:
            print("DEBUG AUTH: Match!")
            return user
        
        if user.password == input_hash.upper():
             print("DEBUG AUTH: Match Upper!")
             return user

        print("DEBUG AUTH: Mismatch")
        return None

    def get_user(self, user_id):
        try:
            return Tercero.objects.get(pk=user_id)
        except Tercero.DoesNotExist:
            return None
