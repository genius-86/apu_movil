import hashlib
from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.encoding import force_bytes

class LegacyMD5PasswordHasher(BasePasswordHasher):
    algorithm = "legacy_md5"

    def verify(self, password, encoded):
        # Encoded in DB might just be the raw hex digest, OR standard django format
        # If legacy, it's likely just the hex digest.
        # But Django expects encoded to include algorithm. 
        # Since we mapped 'password' field to 'clave' column, and 'clave' has plain MD5:
        # We need to handle the case where 'encoded' is just a raw hash.
        
        # Calculate MD5 of provided password
        md5_hash = hashlib.md5(force_bytes(password)).hexdigest()
        
        # Compare
        return encoded == md5_hash

    def safe_summary(self, encoded):
        return {"algorithm": self.algorithm, "hash": encoded}

    def encode(self, password, salt):
        return hashlib.md5(force_bytes(password)).hexdigest()
