import hashlib
import secrets
import base64

class PasswordEncryption:
    """Password encryption menggunakan SHA-256 dengan salt"""
    
    @staticmethod
    def generate_salt(length=32):
        """Generate random salt"""
        return secrets.token_hex(length)
    
    @staticmethod
    def hash_password(password, salt=None):
        """Hash password dengan salt"""
        if salt is None:
            salt = PasswordEncryption.generate_salt()
        
        # Kombinasi password + salt
        salted_password = password + salt
        
        # Hash menggunakan SHA-256
        hash_obj = hashlib.sha256(salted_password.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        
        return password_hash, salt
    
    @staticmethod
    def verify_password(password, stored_hash, salt):
        """Verify password dengan hash tersimpan"""
        hash_obj = hashlib.sha256((password + salt).encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        
        return password_hash == stored_hash
    
    @staticmethod
    def create_password_entry(password):
        """Buat entry password lengkap (hash + salt)"""
        password_hash, salt = PasswordEncryption.hash_password(password)
        return f"{password_hash}${salt}"
    
    @staticmethod
    def parse_password_entry(entry):
        """Parse entry password menjadi hash dan salt"""
        parts = entry.split('$')
        if len(parts) == 2:
            return parts[0], parts[1]
        return None, None
    
    @staticmethod
    def validate_password_strength(password):
        """Validasi kekuatan password"""
        if len(password) < 6:
            return False, "Password minimal 6 karakter"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_upper or has_lower):
            return False, "Password harus mengandung huruf"
        
        return True, "Password valid"

class DataEncryption:
    """Simple encryption untuk data sensitif"""
    
    @staticmethod
    def xor_encrypt(data, key):
        """XOR encryption sederhana"""
        encrypted = bytearray()
        key_bytes = key.encode('utf-8')
        key_length = len(key_bytes)
        
        for i, byte in enumerate(data.encode('utf-8')):
            encrypted.append(byte ^ key_bytes[i % key_length])
        
        return base64.b64encode(encrypted).decode('utf-8')
    
    @staticmethod
    def xor_decrypt(encrypted_data, key):
        """XOR decryption"""
        try:
            encrypted = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted = bytearray()
            key_bytes = key.encode('utf-8')
            key_length = len(key_bytes)
            
            for i, byte in enumerate(encrypted):
                decrypted.append(byte ^ key_bytes[i % key_length])
            
            return decrypted.decode('utf-8')
        except:
            return None