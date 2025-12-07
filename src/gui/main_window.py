import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.book_management import BookManagementWindow
from gui.transaction_window import TransactionWindow
from gui.analytics_window import AnalyticsWindow

class MainWindow:
    """Main window aplikasi perpustakaan"""
    
    def __init__(self, library_system, on_logout):
        self.library = library_system
        self.on_logout = on_logout
        
        self.root = tk.Tk()
        self.root.title("Sistem Perpustakaan - Dashboard")
        self.root.geometry("1000x700")
        
        # Center window
        self.center_window()
        
        self.create_widgets()
        self.refresh_data()
    
    def center_window(self):
        """Center window di layar"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Buat komponen UI"""
        # Top bar
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        user_info = f"User: {self.library.current_user.username} ({self.library.current_user.role})"
        ttk.Label(
            top_frame,
            text=user_info,
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            top_frame,
            text="Logout",
            command=self.handle_logout
        ).pack(side=tk.RIGHT)
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Menu
        left_panel = ttk.Frame(main_container, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Label(
            left_panel,
            text="📚 MENU",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Menu buttons
        menu_buttons = []
        
        menu_buttons.append(("🏠 Dashboard", self.show_dashboard))
        menu_buttons.append(("📖 Daftar Buku", self.show_books))
        menu_buttons.append(("🔍 Cari Buku", self.show_search))
        
        if self.library.is_admin():
            menu_buttons.append(("📝 Kelola Buku", self.show_book_management))
            menu_buttons.append(("✅ Proses Transaksi", self.show_transaction_management))
            menu_buttons.append(("📊 Analytics", self.show_analytics))
        else:
            menu_buttons.append(("📋 Transaksi Saya", self.show_my_transactions))
            menu_buttons.append(("⭐ Rekomendasi", self.show_recommendations))
        
        for text, command in menu_buttons:
            btn = ttk.Button(
                left_panel,
                text=text,
                command=command,
                width=25
            )
            btn.pack(pady=5)
        
        # Right panel - Content
        self.content_frame = ttk.Frame(main_container)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def clear_content(self):
        """Bersihkan content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Tampilkan dashboard"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="Dashboard",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Statistics
        stats = self.library.get_statistics()
        
        stats_frame = ttk.LabelFrame(self.content_frame, text="Statistik Perpustakaan", padding="20")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_text = f"""
Total Buku: {stats['total_books']}
Buku Tersedia: {stats['available_books']}
Buku Dipinjam: {stats['borrowed_books']}
Total User: {stats['total_users']}
Transaksi Pending: {stats['pending_transactions']}
        """
        
        ttk.Label(
            stats_frame,
            text=info_text,
            font=("Arial", 11),
            justify=tk.LEFT
        ).pack()
        
        # Popular books
        popular_frame = ttk.LabelFrame(self.content_frame, text="Buku Populer", padding="20")
        popular_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        popular_books = self.library.get_popular_books(5)
        
        if popular_books:
            for i, (book, count) in enumerate(popular_books, 1):
                text = f"{i}. {book.title} - Dipinjam {count}x"
                ttk.Label(
                    popular_frame,
                    text=text,
                    font=("Arial", 10)
                ).pack(anchor=tk.W, pady=2)
        else:
            ttk.Label(
                popular_frame,
                text="Belum ada data peminjaman",
                font=("Arial", 10)
            ).pack()
    
    def show_books(self):
        """Tampilkan daftar buku"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="Daftar Buku",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Treeview
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        columns = ("ID", "Title", "Author", "Genre", "Year", "Stock")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.column("Title", width=250)
        tree.column("Author", width=150)
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load books
        books = self.library.get_all_books()
        for book in books:
            tree.insert('', tk.END, values=(
                book.books_id,
                book.title,
                book.author,
                book.genre,
                book.year or "",
                book.stock
            ))
        
        # Actions
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def request_borrow():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Pilih buku terlebih dahulu!")
                return
            
            values = tree.item(selection[0])['values']
            book_id = values[0]
            
            success, message = self.library.request_borrow(book_id)
            if success:
                messagebox.showinfo("Success", message)
                self.show_books()
            else:
                messagebox.showerror("Error", message)
        
        if not self.library.is_admin():
            ttk.Button(
                action_frame,
                text="Pinjam Buku",
                command=request_borrow
            ).pack(side=tk.LEFT, padx=5)
    
    def show_search(self):
        """Tampilkan form pencarian"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="Pencarian Buku",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Search form
        search_frame = ttk.Frame(self.content_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="Cari (judul/penulis/genre/ISBN):").pack(side=tk.LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Results
        results_frame = ttk.Frame(self.content_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        results_text = scrolledtext.ScrolledText(results_frame, height=20, font=("Arial", 10))
        results_text.pack(fill=tk.BOTH, expand=True)
        
        def do_search():
            query = search_entry.get().strip()
            if not query:
                messagebox.showwarning("Warning", "Masukkan kata kunci pencarian!")
                return
            
            results = self.library.search_books(query)
            results_text.delete(1.0, tk.END)
            
            if results:
                results_text.insert(tk.END, f"Ditemukan {len(results)} buku:\n\n")
                for book in results:
                    info = f"ID: {book.books_id}\n"
                    info += f"Judul: {book.title}\n"
                    info += f"Penulis: {book.author}\n"
                    info += f"Genre: {book.genre}\n"
                    info += f"Tahun: {book.year or '-'}\n"
                    info += f"Stock: {book.stock}\n"
                    info += f"Status: {'Tersedia' if book.is_available() else 'Tidak Tersedia'}\n"
                    info += "-" * 60 + "\n\n"
                    results_text.insert(tk.END, info)
            else:
                results_text.insert(tk.END, "Tidak ada buku yang ditemukan.")
        
        ttk.Button(
            search_frame,
            text="Cari",
            command=do_search
        ).pack(side=tk.LEFT, padx=5)
        
        search_entry.bind('<Return>', lambda e: do_search())
    
    def show_book_management(self):
        """Tampilkan window manajemen buku (admin only)"""
        BookManagementWindow(self.library, self.refresh_data)
    
    def show_transaction_management(self):
        """Tampilkan window manajemen transaksi (admin only)"""
        TransactionWindow(self.library, self.refresh_data)
    
    def show_analytics(self):
        """Tampilkan window analytics (admin only)"""
        AnalyticsWindow(self.library)
    
    def show_my_transactions(self):
        """Tampilkan transaksi user"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="Transaksi Saya",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        history = self.library.get_user_history()
        
        if history:
            text_widget = scrolledtext.ScrolledText(self.content_frame, height=25, font=("Arial", 10))
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            for item in reversed(history):
                trans = item.get('transaction')
                if trans:
                    book = self.library.get_book(trans.book_id)
                    if book:
                        info = f"Transaksi ID: {trans.transaction_id}\n"
                        info += f"Buku: {book.title}\n"
                        info += f"Tipe: {trans.type}\n"
                        info += f"Status: {trans.status}\n"
                        info += f"Waktu: {trans.timestamp}\n"
                        info += "-" * 60 + "\n\n"
                        text_widget.insert(tk.END, info)
        else:
            ttk.Label(
                self.content_frame,
                text="Belum ada transaksi",
                font=("Arial", 11)
            ).pack(pady=50)
    
    def show_recommendations(self):
        """Tampilkan rekomendasi buku"""
        self.clear_content()
        
        ttk.Label(
            self.content_frame,
            text="Rekomendasi Buku",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        recommendations = self.library.get_recommendations(10)
        
        if recommendations:
            for book, score in recommendations:
                book_frame = ttk.LabelFrame(
                    self.content_frame,
                    text=book.title,
                    padding="10"
                )
                book_frame.pack(fill=tk.X, padx=10, pady=5)
                
                info = f"Penulis: {book.author}\n"
                info += f"Genre: {book.genre}\n"
                info += f"Tahun: {book.year or '-'}\n"
                info += f"Score: {score:.2f}"
                
                ttk.Label(book_frame, text=info).pack(anchor=tk.W)
        else:
            ttk.Label(
                self.content_frame,
                text="Belum ada rekomendasi. Pinjam beberapa buku terlebih dahulu!",
                font=("Arial", 11)
            ).pack(pady=50)
    
    def refresh_data(self):
        """Refresh tampilan data"""
        self.show_dashboard()
    
    def handle_logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Yakin ingin logout?"):
            self.library.logout()
            self.root.destroy()
            self.on_logout()
    
    def run(self):
        """Jalankan window"""
        self.root.mainloop()