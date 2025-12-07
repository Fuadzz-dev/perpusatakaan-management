import re

class Validator:
    """Validator untuk input data"""
    
    @staticmethod
    def validate_username(username):
        """Validasi username"""
        if not username:
            return False, "Username tidak boleh kosong"
        
        if len(username) < 3:
            return False, "Username minimal 3 karakter"
        
        if len(username) > 50:
            return False, "Username maksimal 50 karakter"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username hanya boleh huruf, angka, dan underscore"
        
        return True, "Username valid"
    
    @staticmethod
    def validate_password(password):
        """Validasi password"""
        if not password:
            return False, "Password tidak boleh kosong"
        
        if len(password) < 6:
            return False, "Password minimal 6 karakter"
        
        return True, "Password valid"
    
    @staticmethod
    def validate_isbn(isbn):
        """Validasi ISBN"""
        if not isbn:
            return True, "ISBN opsional"
        
        # Remove hyphens and spaces
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        
        if len(isbn_clean) not in [10, 13]:
            return False, "ISBN harus 10 atau 13 digit"
        
        if not isbn_clean.isdigit():
            return False, "ISBN hanya boleh angka"
        
        return True, "ISBN valid"
    
    @staticmethod
    def validate_year(year):
        """Validasi tahun"""
        if not year:
            return True, "Tahun opsional"
        
        try:
            year_int = int(year)
            if year_int < 1000 or year_int > 2100:
                return False, "Tahun harus antara 1000 dan 2100"
            return True, "Tahun valid"
        except ValueError:
            return False, "Tahun harus berupa angka"
    
    @staticmethod
    def validate_stock(stock):
        """Validasi stock"""
        try:
            stock_int = int(stock)
            if stock_int < 0:
                return False, "Stock tidak boleh negatif"
            return True, "Stock valid"
        except ValueError:
            return False, "Stock harus berupa angka"
    
    @staticmethod
    def validate_book_title(title):
        """Validasi judul buku"""
        if not title:
            return False, "Judul tidak boleh kosong"
        
        if len(title) < 1:
            return False, "Judul minimal 1 karakter"
        
        if len(title) > 500:
            return False, "Judul maksimal 500 karakter"
        
        return True, "Judul valid"
    
    @staticmethod
    def validate_author(author):
        """Validasi nama penulis"""
        if not author:
            return True, "Penulis opsional"
        
        if len(author) > 255:
            return False, "Nama penulis maksimal 255 karakter"
        
        return True, "Penulis valid"
    
    @staticmethod
    def validate_genre(genre):
        """Validasi genre"""
        if not genre:
            return True, "Genre opsional"
        
        if len(genre) > 128:
            return False, "Genre maksimal 128 karakter"
        
        return True, "Genre valid"
    
    @staticmethod
    def sanitize_input(input_str):
        """Sanitize input untuk mencegah injection"""
        if not input_str:
            return ""
        
        # Remove special characters yang berbahaya
        sanitized = re.sub(r'[<>\"\'%;()&+]', '', str(input_str))
        return sanitized.strip()
    
    @staticmethod
    def validate_positive_integer(value, field_name="Value"):
        """Validasi integer positif"""
        try:
            int_value = int(value)
            if int_value <= 0:
                return False, f"{field_name} harus lebih dari 0"
            return True, f"{field_name} valid"
        except ValueError:
            return False, f"{field_name} harus berupa angka"
    
    @staticmethod
    def validate_role(role):
        """Validasi role user"""
        valid_roles = ['admin', 'member']
        if role not in valid_roles:
            return False, f"Role harus salah satu dari: {', '.join(valid_roles)}"
        return True, "Role valid"