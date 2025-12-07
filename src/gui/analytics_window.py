import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AnalyticsWindow:
    """Window untuk analytics dan reporting (admin only)"""
    
    def __init__(self, library_system):
        self.library = library_system
        
        if not self.library.is_admin():
            messagebox.showerror("Error", "Hanya admin yang dapat mengakses fitur ini!")
            return
        
        self.window = tk.Toplevel()
        self.window.title("Analytics & Reporting")
        self.window.geometry("900x700")
        
        self.create_widgets()
        self.load_statistics()
    
    def create_widgets(self):
        """Buat komponen UI"""
        # Title
        ttk.Label(
            self.window,
            text="📊 Analytics & Reporting",
            font=("Arial", 18, "bold")
        ).pack(pady=15)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Overview Statistics
        overview_tab = ttk.Frame(notebook, padding="10")
        notebook.add(overview_tab, text="Overview")
        self.create_overview_tab(overview_tab)
        
        # Tab 2: Popular Books
        popular_tab = ttk.Frame(notebook, padding="10")
        notebook.add(popular_tab, text="Popular Books")
        self.create_popular_books_tab(popular_tab)
        
        # Tab 3: Genre Distribution
        genre_tab = ttk.Frame(notebook, padding="10")
        notebook.add(genre_tab, text="Genre Distribution")
        self.create_genre_tab(genre_tab)
        
        # Tab 4: User Statistics
        user_tab = ttk.Frame(notebook, padding="10")
        notebook.add(user_tab, text="User Statistics")
        self.create_user_tab(user_tab)
        
        # Refresh button
        ttk.Button(
            self.window,
            text="🔄 Refresh Data",
            command=self.load_statistics,
            width=20
        ).pack(pady=10)
    
    def create_overview_tab(self, parent):
        """Buat tab overview"""
        # Statistics cards
        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create 4 columns
        for i in range(4):
            cards_frame.columnconfigure(i, weight=1)
        
        self.stat_cards = {}
        stats_info = [
            ("total_books", "📚 Total Buku", "blue"),
            ("available_books", "✅ Tersedia", "green"),
            ("borrowed_books", "📖 Dipinjam", "orange"),
            ("total_users", "👥 Total User", "purple")
        ]
        
        for i, (key, label, color) in enumerate(stats_info):
            card = ttk.LabelFrame(cards_frame, text=label, padding="15")
            card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            
            value_label = ttk.Label(
                card,
                text="0",
                font=("Arial", 24, "bold"),
                foreground=color
            )
            value_label.pack()
            
            self.stat_cards[key] = value_label
        
        # Detailed info
        detail_frame = ttk.LabelFrame(parent, text="Detail Statistik", padding="15")
        detail_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.detail_text = tk.Text(detail_frame, height=15, font=("Arial", 10))
        self.detail_text.pack(fill=tk.BOTH, expand=True)
    
    def create_popular_books_tab(self, parent):
        """Buat tab popular books"""
        ttk.Label(
            parent,
            text="Top 10 Buku Paling Populer",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Treeview
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("Rank", "Title", "Author", "Genre", "Borrow Count")
        self.popular_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        for col in columns:
            self.popular_tree.heading(col, text=col)
            if col == "Title":
                self.popular_tree.column(col, width=250)
            elif col == "Author":
                self.popular_tree.column(col, width=150)
            else:
                self.popular_tree.column(col, width=100)
        
        scrollbar.config(command=self.popular_tree.yview)
        self.popular_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_genre_tab(self, parent):
        """Buat tab genre distribution"""
        ttk.Label(
            parent,
            text="Distribusi Buku per Genre",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Canvas for bar chart
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.genre_canvas = tk.Canvas(canvas_frame, bg="white", height=400)
        self.genre_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Legend/Details
        detail_frame = ttk.Frame(parent)
        detail_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.genre_text = tk.Text(detail_frame, height=8, font=("Arial", 10))
        self.genre_text.pack(fill=tk.BOTH, expand=True)
    
    def create_user_tab(self, parent):
        """Buat tab user statistics"""
        ttk.Label(
            parent,
            text="Statistik User",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # User list
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("User ID", "Username", "Role", "Created At")
        self.user_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=150)
        
        scrollbar.config(command=self.user_tree.yview)
        self.user_tree.pack(fill=tk.BOTH, expand=True)
    
    def load_statistics(self):
        """Load dan tampilkan statistik"""
        stats = self.library.get_statistics()
        
        # Update stat cards
        self.stat_cards['total_books'].config(text=str(stats['total_books']))
        self.stat_cards['available_books'].config(text=str(stats['available_books']))
        self.stat_cards['borrowed_books'].config(text=str(stats['borrowed_books']))
        self.stat_cards['total_users'].config(text=str(stats['total_users']))
        
        # Update detail text
        detail_info = "RINGKASAN PERPUSTAKAAN\n"
        detail_info += "=" * 50 + "\n\n"
        detail_info += f"Total Buku: {stats['total_books']}\n"
        detail_info += f"Buku Tersedia: {stats['available_books']}\n"
        detail_info += f"Buku Dipinjam: {stats['borrowed_books']}\n"
        detail_info += f"Total User: {stats['total_users']}\n"
        detail_info += f"Transaksi Pending: {stats['pending_transactions']}\n\n"
        
        if stats['borrowed_books'] > 0:
            usage_rate = (stats['borrowed_books'] / stats['total_books']) * 100
            detail_info += f"Tingkat Peminjaman: {usage_rate:.1f}%\n"
        
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(1.0, detail_info)
        
        # Load popular books
        self.load_popular_books()
        
        # Load genre distribution
        self.load_genre_distribution(stats['genre_distribution'])
        
        # Load user list
        self.load_user_list()
    
    def load_popular_books(self):
        """Load popular books"""
        self.popular_tree.delete(*self.popular_tree.get_children())
        
        popular = self.library.get_popular_books(10)
        
        for rank, (book, count) in enumerate(popular, 1):
            self.popular_tree.insert('', tk.END, values=(
                rank,
                book.title,
                book.author,
                book.genre,
                count
            ))
    
    def load_genre_distribution(self, genre_dist):
        """Load dan visualisasi genre distribution"""
        self.genre_canvas.delete("all")
        
        if not genre_dist:
            self.genre_canvas.create_text(
                300, 200,
                text="Tidak ada data genre",
                font=("Arial", 12)
            )
            return
        
        # Sort by count
        sorted_genres = sorted(genre_dist.items(), key=lambda x: x[1], reverse=True)
        
        # Bar chart
        canvas_width = self.genre_canvas.winfo_width() or 600
        canvas_height = 350
        
        if len(sorted_genres) > 0:
            max_count = max(count for _, count in sorted_genres)
            bar_width = min(60, (canvas_width - 100) // len(sorted_genres))
            x_offset = 50
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                     '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']
            
            for i, (genre, count) in enumerate(sorted_genres[:10]):
                bar_height = (count / max_count) * (canvas_height - 100)
                x = x_offset + (i * (bar_width + 10))
                y = canvas_height - bar_height - 30
                
                # Draw bar
                color = colors[i % len(colors)]
                self.genre_canvas.create_rectangle(
                    x, y,
                    x + bar_width, canvas_height - 30,
                    fill=color, outline="black"
                )
                
                # Draw count
                self.genre_canvas.create_text(
                    x + bar_width/2, y - 10,
                    text=str(count),
                    font=("Arial", 9, "bold")
                )
                
                # Draw genre label (rotated)
                label = genre[:10] if len(genre) > 10 else genre
                self.genre_canvas.create_text(
                    x + bar_width/2, canvas_height - 15,
                    text=label,
                    font=("Arial", 8),
                    angle=45
                )
        
        # Update genre text
        self.genre_text.delete(1.0, tk.END)
        genre_info = "DISTRIBUSI GENRE\n" + "=" * 40 + "\n\n"
        for genre, count in sorted_genres:
            percentage = (count / sum(genre_dist.values())) * 100
            genre_info += f"{genre}: {count} buku ({percentage:.1f}%)\n"
        
        self.genre_text.insert(1.0, genre_info)
    
    def load_user_list(self):
        """Load user list"""
        self.user_tree.delete(*self.user_tree.get_children())
        
        users = self.library.users_hash.get_all()
        
        for user_id, user in users:
            self.user_tree.insert('', tk.END, values=(
                user.user_id,
                user.username,
                user.role,
                user.created_at[:10] if user.created_at else ""
            ))