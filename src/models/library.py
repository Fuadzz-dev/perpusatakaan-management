import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures.queue import Queue
from data_structures.stack import Stack
from data_structures.graph import Graph
from models.book import Book
from models.user import User
from models.transaction import Transaction, BorrowHistory
from utils.encryption import PasswordEncryption
from utils.database_connector import DatabaseConnector
from datetime import datetime

class Library:
    """Sistem perpustakaan utama dengan semua fitur"""
    
    def __init__(self):
        # Data structures
        self.transaction_queue = Queue()
        self.history_stack = Stack()
        self.recommendation_graph = Graph()
        
        # Database Connector
        self.db = DatabaseConnector(
            host="localhost",
            user="root",
            password="",
            database="perpustakaan_db" # ✅ FIXED: Menggunakan nama database yang konsisten
        )
        if not self.db.connect():
            raise ConnectionError("Gagal terhubung ke database. Pastikan XAMPP MySQL berjalan dan database ada.")
        
        # Current user
        self.current_user = None
        
        # Load data
        self.initialize_data()
    
    # ==================== USER MANAGEMENT ====================
    
    def register_user(self, username, password, role='member'):
        """Register user baru"""
        query_check = "SELECT user_id FROM users WHERE username = %s"
        if self.db.execute_query(query_check, (username,), fetch='one'):
            return False, "Username sudah digunakan"
        
        password_entry = PasswordEncryption.create_password_entry(password)
        
        query_insert = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
        user_id = self.db.execute_query(query_insert, (username, password_entry, role))
        
        return (True, "Registrasi berhasil") if user_id else (False, "Gagal mendaftar ke database.")
    
    def login(self, username, password):
        """Login user"""
        query = "SELECT * FROM users WHERE username = %s"
        user_data = self.db.execute_query(query, (username,), fetch='one')
        
        if user_data:
            user = User.from_dict(user_data)
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
        
        query = """
            INSERT INTO books (title, author, isbn, genre, year, stock, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (title, author, isbn, genre, year, stock, description)
        book_id = self.db.execute_query(query, params)
        
        return (True, "Buku berhasil ditambahkan") if book_id else (False, "Gagal menambahkan buku.")
    
    def update_book(self, book_id, **kwargs):
        """Update data buku"""
        if not self.is_admin():
            return False, "Hanya admin yang dapat mengupdate buku"
        
        if not self.get_book(book_id):
            return False, "Buku tidak ditemukan"
        
        fields = []
        params = []
        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = %s")
                params.append(value)
        
        if not fields:
            return False, "Tidak ada data untuk diupdate."

        params.append(book_id)
        query = f"UPDATE books SET {', '.join(fields)} WHERE books_id = %s"
        self.db.execute_query(query, tuple(params))
        return True, "Buku berhasil diupdate."
    
    def delete_book(self, book_id):
        """Hapus buku"""
        if not self.is_admin():
            return False, "Hanya admin yang dapat menghapus buku"
        
        if not self.get_book(book_id):
            return False, "Buku tidak ditemukan"
        
        query = "DELETE FROM books WHERE books_id = %s"
        self.db.execute_query(query, (book_id,))
        return True, "Buku berhasil dihapus"
    
    def search_books(self, query):
        """Pencarian multi-kriteria"""
        results = []
        sql_query = """
            SELECT * FROM books 
            WHERE title LIKE %s OR author LIKE %s OR genre LIKE %s OR isbn LIKE %s
        """
        like_query = f"%{query}%"
        params = (like_query, like_query, like_query, like_query)
        
        books_data = self.db.execute_query(sql_query, params, fetch='all')
        if books_data:
            results.extend([Book.from_dict(data) for data in books_data])

        try:
            book_id = int(query)
            book = self.get_book(book_id)
            if book and book not in results:
                results.append(book)
        except ValueError:
            pass
        return results
    
    def get_all_books(self):
        """Dapatkan semua buku"""
        books_data = self.db.execute_query("SELECT * FROM books ORDER BY title", fetch='all')
        return [Book.from_dict(data) for data in books_data] if books_data else []
    
    def get_book(self, book_id):
        """Dapatkan buku berdasarkan ID"""
        book_data = self.db.execute_query("SELECT * FROM books WHERE books_id = %s", (book_id,), fetch='one')
        return Book.from_dict(book_data) if book_data else None
    
    # ==================== TRANSACTION MANAGEMENT ====================
    
    def request_borrow(self, book_id):
        """Request peminjaman buku"""
        if not self.current_user:
            return False, "Anda harus login terlebih dahulu"
        
        book = self.get_book(book_id)
        if not book:
            return False, "Buku tidak ditemukan"
        
        if not book.is_available():
            return False, "Buku tidak tersedia"
        
        query = "INSERT INTO transactions (user_id, book_id, type, status) VALUES (%s, %s, %s, %s)"
        params = (self.current_user.user_id, book_id, 'borrow', 'pending')  # ✅ FIXED: Tipe transaksi harus 'borrow'
        trans_id = self.db.execute_query(query, params)
        
        if not trans_id:
            return False, "Gagal mengajukan permintaan"

        transaction = Transaction(trans_id, self.current_user.user_id, book_id, 'borrow')  # ✅ FIXED: Tipe transaksi harus 'borrow'
        self.transaction_queue.enqueue(transaction)
        return True, "Permintaan peminjaman berhasil diajukan"
    
    def request_return(self, book_id):
        """Request pengembalian buku"""
        if not self.current_user:
            return False, "Anda harus login terlebih dahulu"
        
        history_data = self.db.execute_query( # Menggunakan tabel 'history'
            "SELECT * FROM history WHERE user_id = %s AND book_id = %s AND return_date IS NULL",
            (self.current_user.user_id, book_id),
            fetch='one'
        )
        
        if not history_data:
            return False, "Anda tidak sedang meminjam buku ini"
        
        query = "INSERT INTO transactions (user_id, book_id, type, status) VALUES (%s, %s, %s, %s)"
        params = (self.current_user.user_id, book_id, 'return', 'pending')
        trans_id = self.db.execute_query(query, params)
        
        if not trans_id:
            return False, "Gagal mengajukan permintaan"
        
        transaction = Transaction(trans_id, self.current_user.user_id, book_id, 'return')
        self.transaction_queue.enqueue(transaction)
        return True, "Permintaan pengembalian berhasil diajukan"
    
    def process_transaction(self):
        """Process transaksi dari queue (admin only)"""
        if not self.is_admin():
            return False, "Hanya admin yang dapat memproses transaksi"
        
        if self.transaction_queue.is_empty():
            return False, "Tidak ada transaksi untuk diproses"
        
        transaction = self.transaction_queue.dequeue()
        book = self.get_book(transaction.book_id)
        
        if not book:
            self.db.execute_query("UPDATE transactions SET status = 'failed' WHERE transaction_id = %s", (transaction.transaction_id,))
            return False, f"Buku dengan ID {transaction.book_id} tidak ditemukan. Transaksi dibatalkan."
        
        if transaction.is_borrow():
            if book.borrow():
                transaction.approve()
                
                # Update di DB
                self.db.execute_query("UPDATE books SET stock = stock - 1 WHERE books_id = %s", (book.books_id,))
                self.db.execute_query("UPDATE transactions SET status = 'approved' WHERE transaction_id = %s", (transaction.transaction_id,))
                self.db.execute_query("INSERT INTO history (user_id, book_id) VALUES (%s, %s)", (transaction.user_id, transaction.book_id)) # Menggunakan tabel 'history'

                # Save to stack for undo
                self.history_stack.push({
                    'action': 'borrow',
                    'transaction': transaction
                })
                
                # Update recommendation graph
                self._update_recommendation_graph(transaction.user_id, transaction.book_id)
                return True, "Peminjaman berhasil diproses"
            else:
                transaction.reject()
                self.db.execute_query("UPDATE transactions SET status = 'rejected' WHERE transaction_id = %s", (transaction.transaction_id,))
                return False, "Buku tidak tersedia"
        
        elif transaction.is_return():
            book.return_book()
            transaction.approve()
            
            # Update di DB
            self.db.execute_query("UPDATE books SET stock = stock + 1 WHERE books_id = %s", (book.books_id,))
            self.db.execute_query("UPDATE transactions SET status = 'approved' WHERE transaction_id = %s", (transaction.transaction_id,))
            self.db.execute_query("UPDATE history SET return_date = %s WHERE user_id = %s AND book_id = %s AND return_date IS NULL", (datetime.now(), transaction.user_id, transaction.book_id)) # Menggunakan tabel 'history'
            
            self.history_stack.push({
                'action': 'return',
                'transaction': transaction
            })
            return True, "Pengembalian berhasil diproses"
        
        return False, "Jenis transaksi tidak valid"
    
    def get_pending_transactions(self):
        """Dapatkan semua transaksi pending"""
        return self.transaction_queue.get_all()
    
    def get_user_history(self, user_id=None):
        """Dapatkan history peminjaman user - FIXED"""
        if user_id is None and self.current_user:
            user_id = self.current_user.user_id
        
        query = """
            SELECT t.*, b.title as book_title 
            FROM transactions t
            LEFT JOIN books b ON t.book_id = b.books_id
            WHERE t.user_id = %s 
            ORDER BY t.timestamp DESC
        """
        trans_data = self.db.execute_query(query, (user_id,), fetch='all')
        
        if not trans_data:
            return []
        
        # ✅ FIXED: Konversi ke format yang benar
        result = []
        for t_dict in trans_data:
            transaction = Transaction.from_dict(t_dict)
            result.append({
                'transaction': transaction,
                'book_title': t_dict.get('book_title', 'Unknown')
            })
        
        return result
    
    # ==================== RECOMMENDATION SYSTEM ====================
    
    def _update_recommendation_graph(self, user_id, book_id):
        """Update graph untuk sistem rekomendasi"""
        user_vertex = f"user_{user_id}"
        book_vertex = f"book_{book_id}"
        
        self.recommendation_graph.add_vertex(user_vertex)
        self.recommendation_graph.add_edge(user_vertex, book_vertex, weight=1.0)
        
        all_users = self.db.execute_query("SELECT user_id FROM users", fetch='all')
        for user in all_users:
            if user['user_id'] != user_id:
                other_vertex = f"user_{user['user_id']}"
                other_books = self.recommendation_graph.get_neighbors(other_vertex)
                
                if book_vertex in other_books:
                    similarity = self.recommendation_graph.get_weight(user_vertex, other_vertex) + 0.2
                    self.recommendation_graph.add_undirected_edge(
                        user_vertex, other_vertex, weight=similarity
                    )
    
    def get_recommendations(self, top_n=5):
        """Dapatkan rekomendasi buku untuk current user"""
        if not self.current_user:
            return []
        
        user_vertex = f"user_{self.current_user.user_id}"
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
        
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        result = []
        for book_id, score in sorted_recs[:top_n]:
            book = self.get_book(book_id)
            if book:
                result.append((book, score))
        
        return result
    
    # ==================== ANALYTICS ====================
    
    def get_statistics(self):
        """Dapatkan statistik perpustakaan - FIXED"""
        total_books_result = self.db.execute_query("SELECT COUNT(*) as c FROM books", fetch='one')
        total_books = total_books_result['c'] if total_books_result else 0
        
        total_users_result = self.db.execute_query("SELECT COUNT(*) as c FROM users", fetch='one')
        total_users = total_users_result['c'] if total_users_result else 0
        
        pending_transactions = self.transaction_queue.get_size()
        
        available_books_result = self.db.execute_query("SELECT SUM(stock) as s FROM books", fetch='one')
        available_books = available_books_result['s'] if available_books_result and available_books_result['s'] else 0
        
        # ✅ FIXED: Hitung borrowed books dengan benar
        borrowed_books_result = self.db.execute_query(
            "SELECT COUNT(*) as c FROM history WHERE return_date IS NULL", # Menggunakan tabel 'history'
            fetch='one'
        )
        borrowed_books = borrowed_books_result['c'] if borrowed_books_result else 0
        
        # Genre statistics
        genre_count = {}
        genre_data = self.db.execute_query("SELECT genre, COUNT(*) as count FROM books GROUP BY genre", fetch='all')
        if genre_data:
            for item in genre_data:
                genre = item['genre'] or "Unknown"
                genre_count[genre] = item['count']
        
        # ✅ FIXED: Return data yang benar
        return {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,  # ✅ FIXED
            'total_users': total_users,
            'pending_transactions': pending_transactions,
            'genre_distribution': genre_count
        }
    
    def get_popular_books(self, top_n=10):
        """Dapatkan buku paling populer"""
        query = """
            SELECT b.*, COUNT(bh.book_id) as borrow_count
            FROM history bh
            JOIN books b ON bh.book_id = b.books_id
            GROUP BY bh.book_id
            ORDER BY borrow_count DESC
            LIMIT %s
        """
        popular_data = self.db.execute_query(query, (top_n,), fetch='all')
        
        result = []
        if popular_data:
            for item in popular_data:
                book = Book.from_dict(item)
                result.append((book, item['borrow_count']))
        
        return result
    
    # ==================== DATA PERSISTENCE ====================
    
    def initialize_data(self):
        """Inisialisasi data dari database saat startup"""
        print("Menginisialisasi data dari database...")
        
        trans_data = self.db.execute_query("SELECT * FROM transactions WHERE status = 'pending'", fetch='all')
        if trans_data:
            print(f"Memuat {len(trans_data)} transaksi yang tertunda...")
            for t_dict in trans_data:
                transaction = Transaction.from_dict(t_dict)
                self.transaction_queue.enqueue(transaction)
        
        user_count_result = self.db.execute_query("SELECT COUNT(*) as c FROM users", fetch='one')
        user_count = user_count_result['c'] if user_count_result else 0
        
        if user_count == 0:
            print("Database pengguna kosong. Membuat pengguna default...")
            self.register_user('admin', 'admin123', 'admin')
            self.register_user('user', 'user123', 'member')