from datetime import datetime

class User:
    """Model untuk user"""
    
    def __init__(self, user_id, username, password_hash, role='member', created_at=None):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at if created_at else datetime.now().isoformat()
    
    def to_dict(self):
        """Convert ke dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password_hash': self.password_hash,
            'role': self.role,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        """Create User dari dictionary"""
        return User(
            user_id=data.get('user_id'),
            username=data.get('username', ''),
            password_hash=data.get('password_hash', ''),
            role=data.get('role', 'member'),
            created_at=data.get('created_at')
        )
    
    def is_admin(self):
        """Cek apakah user adalah admin"""
        return self.role == 'admin'
    
    def is_member(self):
        """Cek apakah user adalah member"""
        return self.role == 'member'
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def __repr__(self):
        return f"User(id={self.user_id}, username='{self.username}', role='{self.role}')"