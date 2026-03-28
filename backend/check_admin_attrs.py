import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apu_backend.settings')
django.setup()

from core.models import Tercero

def check_admin_attributes():
    print("Checking admin attributes on Tercero model...")
    
    # Try to find a superuser
    superuser = Tercero.objects.filter(super_usuario='S').first()
    if superuser:
        print(f"Found superuser: {superuser}")
        print(f"is_staff: {superuser.is_staff}")
        print(f"is_superuser: {superuser.is_superuser}")
        print(f"is_active: {superuser.is_active}")
        print(f"has_perm('any'): {superuser.has_perm('any')}")
        print(f"has_module_perms('app'): {superuser.has_module_perms('app')}")
        
        if not superuser.is_staff or not superuser.is_superuser:
            print("ERROR: Superuser attributes incorrect!")
        else:
            print("SUCCESS: Superuser attributes correct.")
    else:
        print("WARNING: No superuser found with super_usuario='S' to test.")

    # Try to find a normal user
    normal_user = Tercero.objects.filter(super_usuario='N').first()
    if normal_user:
        print(f"Found normal user: {normal_user}")
        print(f"is_staff: {normal_user.is_staff}")
        print(f"is_superuser: {normal_user.is_superuser}")
        
        if normal_user.is_staff or normal_user.is_superuser:
            print("ERROR: Normal user attributes incorrect!")
        else:
            print("SUCCESS: Normal user attributes correct.")
    else:
        print("WARNING: No normal user found with super_usuario='N' to test.")

if __name__ == "__main__":
    check_admin_attributes()
