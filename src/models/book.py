class Book:
    """Model untuk buku"""
    
    def __init__(self, books_id, title, author="", isbn="", genre="", 
                 year=None, stock=1, description=""):
        self.books_id = books_id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.stock = stock
        self.description = description
    
    def to_dict(self):
        """Convert ke dictionary"""
        return {
            'books_id': self.books_id,
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'year': self.year,
            'stock': self.stock,
            'description': self.description
        }
    
    @staticmethod
    def from_dict(data):
        """Create Book dari dictionary"""
        return Book(
            books_id=data.get('books_id'),
            title=data.get('title', ''),
            author=data.get('author', ''),
            isbn=data.get('isbn', ''),
            genre=data.get('genre', ''),
            year=data.get('year'),
            stock=data.get('stock', 1),
            description=data.get('description', '')
        )
    
    def is_available(self):
        """Cek apakah buku tersedia"""
        return self.stock > 0
    
    def borrow(self):
        """Kurangi stock saat dipinjam"""
        if self.stock > 0:
            self.stock -= 1
            return True
        return False
    
    def return_book(self):
        """Tambah stock saat dikembalikan"""
        self.stock += 1
    
    def matches_search(self, query):
        """Cek apakah buku cocok dengan query pencarian"""
        query_lower = query.lower()
        return (query_lower in self.title.lower() or
                query_lower in self.author.lower() or
                query_lower in self.genre.lower() or
                query_lower in self.isbn.lower())
    
    def __str__(self):
        return f"{self.title} by {self.author} ({self.year})"
    
    def __repr__(self):
        return f"Book(id={self.books_id}, title='{self.title}')"