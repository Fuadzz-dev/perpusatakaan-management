import mysql.connector
from mysql.connector import Error

class DatabaseConnector:
    """Menangani koneksi dan operasi ke database MySQL."""

    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None

    def connect(self):
        """Membuat koneksi ke database."""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Berhasil terhubung ke database MySQL")
                return True
        except Error as e:
            print(f"Error saat menghubungkan ke MySQL: {e}")
            self.connection = None
            return False

    def disconnect(self):
        """Menutup koneksi database."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Koneksi MySQL ditutup")

    def execute_query(self, query, params=None, fetch=None):
        """
        Menjalankan query.
        :param query: String query SQL.
        :param params: Tuple parameter untuk query.
        :param fetch: 'one', 'all', atau None (untuk INSERT, UPDATE, DELETE).
        :return: Hasil query jika ada, atau lastrowid.
        """
        if not self.connection or not self.connection.is_connected():
            print("Tidak ada koneksi ke database.")
            if not self.connect():
                return None

        cursor = self.connection.cursor(dictionary=True) # Menggunakan dictionary cursor
        result = None
        try:
            cursor.execute(query, params or ())
            if fetch == 'one':
                result = cursor.fetchone()
            elif fetch == 'all':
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.lastrowid # Berguna untuk mendapatkan ID setelah INSERT
        except Error as e:
            print(f"Error saat menjalankan query: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
        return result

    def test_connection(self):
        """Tes koneksi ke database."""
        if self.connect():
            self.disconnect()
            return True
        return False

# Konfigurasi default untuk XAMPP
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "library_system"
}