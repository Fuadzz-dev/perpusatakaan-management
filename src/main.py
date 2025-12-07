#!/usr/bin/env python3
"""
SISTEM PERPUSTAKAAN - Library Management System
Menggunakan struktur data: BST, Hash Table, Queue, Stack, Graph, Linked List
"""

import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.library import Library
from gui.login_window import LoginWindow
from gui.main_window import MainWindow

class LibraryApplication:
    """Main application class"""
    
    def __init__(self):
        self.library = Library()
        self.start()
    
    def start(self):
        """Start aplikasi dengan login window"""
        login_window = LoginWindow(self.library, self.on_login_success)
        login_window.run()
    
    def on_login_success(self):
        """Callback setelah login berhasil"""
        main_window = MainWindow(self.library, self.on_logout)
        main_window.run()
    
    def on_logout(self):
        """Callback setelah logout"""
        self.start()

def main():
    """Entry point aplikasi"""
    print("=" * 60)
    print("SISTEM PERPUSTAKAAN - Library Management System")
    print("=" * 60)
    print("\nMemuat aplikasi...")
    print("\nFitur Utama:")
    print("✓ Manajemen Buku (BST + Hash Table)")
    print("✓ Sistem Transaksi (Queue + Stack)")
    print("✓ Pencarian Multi-Kriteria (Tree Traversal)")
    print("✓ Sistem Rekomendasi (Graph Algorithms)")
    print("✓ Manajemen User (Hash Table + Encryption)")
    print("✓ Analytics & Reporting")
    print("\nDefault Credentials:")
    print("  Admin - Username: admin, Password: admin123")
    print("  User  - Username: user, Password: user123")
    print("=" * 60)
    print()
    
    try:
        app = LibraryApplication()
    except KeyboardInterrupt:
        print("\n\nAplikasi dihentikan oleh user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()