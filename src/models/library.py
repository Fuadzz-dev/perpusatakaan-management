import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures.bst import BST
from data_structures.hash_table import HashTable
from data_structures.queue import Queue
from data_structures.stack import Stack
from data_structures.graph import Graph
from models.book import Book
from models.user import User
from models.transaction import Transaction, BorrowHistory
from utils.file_handler import FileHandler
from utils.encryption import PasswordEncryption
from datetime import datetime

class Library:
    """Sistem perpustakaan utama dengan semua fitur"""
    
    def __init__(self):
        # Data structures
        self.books_bst = BST()  # BST untuk pencarian buku berdasarkan ID
        self.books_hash = HashTable()  # Hash table untuk akses cepat
        self.users_hash = HashTable()  # Hash table untuk user management
        self.transaction_queue = Queue()  # Queue untuk antrian transaksi
        self.history_stack = Stack()  # Stack untuk undo operations
        self.recommendation_graph = Graph()  # Graph untuk sistem rekomendasi
        
        # File handler
        self.file_handler = FileHandler()
        
        # Counters
        self.next_book_id = 1
        self.next_user_id = 1
        self.next_transaction_id = 1
        self.next_history_id = 1
        
        # Current user
        self.current_user = None
        
        # Load data
        self.load_all_data()
    
    # ==================== USER MANAGEMENT ====================
    
    def register_user(self, username, password, role='member'):
        """Register user baru"""
        # Cek apakah username sudah ada
        for _, user in self.users_hash.get_all():
            if user.username == username:
                return False, "Username sudah digunakan"
        
        # Encrypt password
        password_entry = PasswordEncryption.create_password_entry(password)
        
        # Buat user baru
        user = User(self.next_user_id, username, password_entry, role)
        self.users_hash.insert(self.next_user_id, user)
        self.next_user_id += 1
        
        self.save_users()
        return True, "Registrasi berhasil"
    
    def login(self, username, password):
        """Login user"""
        for user_id, user in self.users_hash.get_all():
            if user.username == username:
                password_hash, salt = PasswordEncryption.parse_password_entry(user.password_hash)
                if password_hash and PasswordEncryption.verify_password(password, password_hash, salt):
                    self.current_user = user
                    return True, f"Login berhasil sebagai {user.role}"
                return False, "Password salah"
        return False, "Username tidak ditemukan"
    
    def logout(self):
        """Logout user"""
        self.current_user = None
    
    def is_admin(self):
        """Cek apakah current user adalah admin"""
        return self.current_user and self.current_user.is_admin()
    
    # ==================== BOOK MANAGEMENT ====================
    
    def add_book(self, title, author="", isbn="", genre="", year=None, stock=1, description=""):
        """Tambah buku baru (admin only)"""
        if not self.is_admin():
            return False, "Hanya admin yang dapat menambah buku"
        
        book = Book(self.next_book_id, title, author, isbn, genre, year, stock, description)
        
        # Insert ke BST dan Hash Table
        self.books_bst.insert(self.next_book_id, book)
        self.books_hash.insert(self.next_book_id, book)
        
        # Add to recommendation graph
        self.recommendation_graph.add_vertex(f"book_{self.next_book_id}")
        
        # Build relationships based on genre
        for book_id, existing_book in self.books_hash.get_all():
            if book_id != self.next_book_id and existing_book.genre == book.genre:
                self.recommendation_graph.add_undirected_edge(
                    f"book_{self.next_book_id}", 
                    f"book_{book_id}", 
                    weight=0.8
                )
        
        self.next_book_id += 1
        self.save_books()
        
        return True, "Buku berhasil ditambahkan"
    
    def update_book(self, book_id, **kwargs):
        """Update data buku"""
        if not self.is_admin():
            return False, "Hanya admin yang dapat mengupdate buku"
        
        book = self.books_hash.search(book_id)
        if not book:
            return False, "Buku tidak ditemukan"
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(book, key) and value is not None:
                setattr(book, key, value)
        
        self.save_books()
        return True, "Buku berhasil diupdate"
    
    def delete_book(self, book_id):
        """Hapus buku"""
        if not self.is_admin():
            return False, "Hanya admin yang dapat menghapus buku"
        
        book = self.books_hash.search(book_id)
        if not book:
            return False, "Buku tidak ditemukan"
        
        self.books_bst.delete(book_id)
        self.books_hash.delete(book_id)
        self.save_books()
        
        return True, "Buku berhasil dihapus"
    
    def search_books(self, query):
        """Pencarian multi-kriteria menggunakan BST traversal dan hashing"""
        results = []
        
        # Search by ID (exact match using hash)
        try:
            book_id = int(query)
            book = self.books_hash.search(book_id)
            if book:
                results.append(book)
        except ValueError:
            pass
        
        # Search by title, author, genre (using BST traversal)
        all_books = self.books_bst.get_all()
        for book_id, book in all_books:
            if book.matches_search(query) and book not in results:
                results.append(book)
        
        return results
    
    def get_all_books(self):
        """Dapatkan semua buku"""
        return [book for _, book in self.books_bst.get_all()]
    
    def get_book(self, book_id):
        """Dapatkan buku berdasarkan ID"""
        return self.books_hash.search(book_id)
    
    # ==================== TRANSACTION MANAGEMENT ====================
    
    def request_borrow(self, book_id):
        """Request peminjaman buku"""
        if not self.current_user:
            return False, "Anda harus login terlebih dahulu"
        
        book = self.books_hash.search(book_id)
        if not book:
            return False, "Buku tidak ditemukan"
        
        if not book.is_available():
            return False, "Buku tidak tersedia"
        
        # Buat transaksi dan masukkan ke queue
        transaction = Transaction(
            self.next_transaction_id,
            self.current_user.user_id,
            book_id,
            'borrow'
        )
        
        self.transaction_queue.enqueue(transaction)
        self.next_transaction_id += 1
        self.save_transactions()
        
        return True, "Permintaan peminjaman berhasil diajukan"
    
    def request_return(self, book_id):
        """Request pengembalian buku"""
        if not self.current_user:
            return False, "Anda harus login terlebih dahulu"
        
        book = self.books_hash.search(book_id)
        if not book:
            return False, "Buku tidak ditemukan"
        
        # Buat transaksi dan masukkan ke queue
        transaction = Transaction(
            self.next_transaction_id,
            self.current_user.user_id,
            book_id,
            'return'
        )
        
        self.transaction_queue.enqueue(transaction)
        self.next_transaction_id += 1
        self.save_transactions()
        
        return True, "Permintaan pengembalian berhasil diajukan"
    
    def process_transaction(self):
        """Process transaksi dari queue (admin only)"""
        if not self.is_admin():
            return False, "Hanya admin yang dapat memproses transaksi"
        
        if self.transaction_queue.is_empty():
            return False, "Tidak ada transaksi untuk diproses"
        
        transaction = self.transaction_queue.dequeue()
        book = self.books_hash.search(transaction.book_id)
        
        if not book:
            return False, "Buku tidak ditemukan"
        
        if transaction.is_borrow():
            if book.borrow():
                transaction.approve()
                # Buat history
                history = BorrowHistory(
                    self.next_history_id,
                    transaction.user_id,
                    transaction.book_id
                )
                self.next_history_id += 1
                
                # Save to stack for undo
                self.history_stack.push({
                    'action': 'borrow',
                    'transaction': transaction,
                    'history': history
                })
                
                # Update recommendation graph
                self._update_recommendation_graph(transaction.user_id, transaction.book_id)
                
                self.save_books()
                return True, "Peminjaman berhasil diproses"
            else:
                transaction.reject()
                return False, "Buku tidak tersedia"
        
        elif transaction.is_return():
            book.return_book()
            transaction.approve()
            self.history_stack.push({
                'action': 'return',
                'transaction': transaction
            })
            self.save_books()
            return True, "Pengembalian berhasil diproses"
        
        return False, "Jenis transaksi tidak valid"
    
    def get_pending_transactions(self):
        """Dapatkan semua transaksi pending"""
        return self.transaction_queue.get_all()
    
    def get_user_history(self, user_id=None):
        """Dapatkan history peminjaman user"""
        if user_id is None and self.current_user:
            user_id = self.current_user.user_id
        
        history = self.history_stack.get_all()
        user_history = [h for h in history if h.get('transaction', {}).user_id == user_id]
        return user_history
    
    # ==================== RECOMMENDATION SYSTEM ====================
    
    def _update_recommendation_graph(self, user_id, book_id):
        """Update graph untuk sistem rekomendasi"""
        user_vertex = f"user_{user_id}"
        book_vertex = f"book_{book_id}"
        
        self.recommendation_graph.add_vertex(user_vertex)
        self.recommendation_graph.add_edge(user_vertex, book_vertex, weight=1.0)
        
        # Build similarity dengan user lain
        for uid, _ in self.users_hash.get_all():
            if uid != user_id:
                other_vertex = f"user_{uid}"
                other_books = self.recommendation_graph.get_neighbors(other_vertex)
                
                if book_vertex in other_books:
                    # Kedua user pernah pinjam buku yang sama
                    similarity = 0.7
                    self.recommendation_graph.add_undirected_edge(
                        user_vertex, other_vertex, weight=similarity
                    )
    
    def get_recommendations(self, top_n=5):
        """Dapatkan rekomendasi buku untuk current user"""
        if not self.current_user:
            return []
        
        user_vertex = f"user_{self.current_user.user_id}"
        
        # Get books borrowed by similar users (collaborative filtering)
        similar_users = self.recommendation_graph.get_neighbors(user_vertex)
        user_books = self.recommendation_graph.get_neighbors(user_vertex)
        
        recommendations = {}
        
        for similar_user in similar_users:
            if similar_user.startswith('user_'):
                weight = self.recommendation_graph.get_weight(user_vertex, similar_user)
                similar_books = self.recommendation_graph.get_neighbors(similar_user)
                
                for book_vertex in similar_books:
                    if book_vertex.startswith('book_') and book_vertex not in user_books:
                        book_id = int(book_vertex.split('_')[1])
                        if book_id not in recommendations:
                            recommendations[book_id] = 0
                        recommendations[book_id] += weight
        
        # Sort by score
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        # Get book objects
        result = []
        for book_id, score in sorted_recs[:top_n]:
            book = self.books_hash.search(book_id)
            if book:
                result.append((book, score))
        
        return result
    
    # ==================== ANALYTICS ====================
    
    def get_statistics(self):
        """Dapatkan statistik perpustakaan"""
        total_books = len(self.books_hash)
        total_users = len(self.users_hash)
        pending_transactions = self.transaction_queue.get_size()
        
        available_books = sum(1 for _, book in self.books_hash.get_all() if book.is_available())
        borrowed_books = total_books - available_books
        
        # Genre statistics
        genre_count = {}
        for _, book in self.books_hash.get_all():
            genre = book.genre or "Unknown"
            genre_count[genre] = genre_count.get(genre, 0) + 1
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'total_users': total_users,
            'pending_transactions': pending_transactions,
            'genre_distribution': genre_count
        }
    
    def get_popular_books(self, top_n=10):
        """Dapatkan buku paling populer"""
        borrow_count = {}
        
        for history_item in self.history_stack.get_all():
            if 'history' in history_item:
                book_id = history_item['history'].book_id
                borrow_count[book_id] = borrow_count.get(book_id, 0) + 1
        
        sorted_books = sorted(borrow_count.items(), key=lambda x: x[1], reverse=True)
        
        result = []
        for book_id, count in sorted_books[:top_n]:
            book = self.books_hash.search(book_id)
            if book:
                result.append((book, count))
        
        return result
    
    # ==================== DATA PERSISTENCE ====================
    
    def save_books(self):
        """Simpan data buku ke file"""
        books_data = [book.to_dict() for _, book in self.books_hash.get_all()]
        self.file_handler.save_json('books.json', books_data)
    
    def save_users(self):
        """Simpan data user ke file"""
        users_data = [user.to_dict() for _, user in self.users_hash.get_all()]
        self.file_handler.save_json('users.json', users_data)
    
    def save_transactions(self):
        """Simpan data transaksi ke file"""
        transactions_data = [t.to_dict() for t in self.transaction_queue.get_all()]
        self.file_handler.save_json('transactions.json', transactions_data)
    
    def load_all_data(self):
        """Load semua data dari file"""
        # Load books
        books_data = self.file_handler.load_json('books.json', [])
        for book_dict in books_data:
            book = Book.from_dict(book_dict)
            self.books_bst.insert(book.books_id, book)
            self.books_hash.insert(book.books_id, book)
            if book.books_id >= self.next_book_id:
                self.next_book_id = book.books_id + 1
        
        # Load users
        users_data = self.file_handler.load_json('users.json', [])
        for user_dict in users_data:
            user = User.from_dict(user_dict)
            self.users_hash.insert(user.user_id, user)
            if user.user_id >= self.next_user_id:
                self.next_user_id = user.user_id + 1
        
        # Load transactions
        transactions_data = self.file_handler.load_json('transactions.json', [])
        for trans_dict in transactions_data:
            transaction = Transaction.from_dict(trans_dict)
            self.transaction_queue.enqueue(transaction)
            if transaction.transaction_id >= self.next_transaction_id:
                self.next_transaction_id = transaction.transaction_id + 1
        
        # Create default admin if no users
        if len(self.users_hash) == 0:
            self.register_user('admin', 'admin123', 'admin')
            self.register_user('user', 'user123', 'member')