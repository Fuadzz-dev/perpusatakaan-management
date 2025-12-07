import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TransactionWindow:
    """Window untuk manajemen transaksi (admin only)"""
    
    def __init__(self, library_system, on_update_callback=None):
        self.library = library_system
        self.on_update = on_update_callback
        
        if not self.library.is_admin():
            messagebox.showerror("Error", "Hanya admin yang dapat mengakses fitur ini!")
            return
        
        self.window = tk.Toplevel()
        self.window.title("Manajemen Transaksi")
        self.window.geometry("800x600")
        
        self.create_widgets()
        self.refresh_transaction_list()
    
    def create_widgets(self):
        """Buat komponen UI"""
        # Title
        ttk.Label(
            self.window,
            text="Manajemen Transaksi",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Info label
        info_frame = ttk.Frame(self.window)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = ttk.Label(
            info_frame,
            text="",
            font=("Arial", 10),
            foreground="blue"
        )
        self.info_label.pack()
        
        # Transaction list
        list_frame = ttk.LabelFrame(self.window, text="Transaksi Pending", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("Trans ID", "User ID", "Book ID", "Book Title", "Type", "Timestamp")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Book Title":
                self.tree.column(col, width=250)
            else:
                self.tree.column(col, width=100)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            button_frame,
            text="⏭️ Process Next Transaction",
            command=self.process_transaction,
            width=30
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self.refresh_transaction_list,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="❌ Close",
            command=self.window.destroy,
            width=15
        ).pack(side=tk.RIGHT, padx=5)
        
        # Details frame
        details_frame = ttk.LabelFrame(self.window, text="Detail Transaksi", padding="10")
        details_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.details_text = tk.Text(details_frame, height=8, font=("Arial", 10))
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_transaction_select)
    
    def refresh_transaction_list(self):
        """Refresh daftar transaksi"""
        self.tree.delete(*self.tree.get_children())
        self.details_text.delete(1.0, tk.END)
        
        transactions = self.library.get_pending_transactions()
        
        self.info_label.config(text=f"Total transaksi pending: {len(transactions)}")
        
        for trans in transactions:
            book = self.library.get_book(trans.book_id)
            book_title = book.title if book else "Unknown"
            
            self.tree.insert('', tk.END, values=(
                trans.transaction_id,
                trans.user_id,
                trans.book_id,
                book_title,
                trans.type,
                trans.timestamp
            ))
    
    def on_transaction_select(self, event):
        """Handle pemilihan transaksi"""
        selection = self.tree.selection()
        if not selection:
            return
        
        values = self.tree.item(selection[0])['values']
        trans_id = values[0]
        user_id = values[1]
        book_id = values[2]
        
        # Get details
        transactions = self.library.get_pending_transactions()
        trans = None
        for t in transactions:
            if t.transaction_id == trans_id:
                trans = t
                break
        
        if not trans:
            return
        
        book = self.library.get_book(book_id)
        user = self.library.users_hash.search(user_id)
        
        details = "="*50 + "\n"
        details += f"Transaction ID: {trans.transaction_id}\n"
        details += f"Type: {trans.type.upper()}\n"
        details += f"Status: {trans.status}\n"
        details += f"Timestamp: {trans.timestamp}\n"
        details += "="*50 + "\n\n"
        
        if user:
            details += f"User ID: {user.user_id}\n"
            details += f"Username: {user.username}\n"
            details += f"Role: {user.role}\n\n"
        
        if book:
            details += f"Book ID: {book.books_id}\n"
            details += f"Title: {book.title}\n"
            details += f"Author: {book.author}\n"
            details += f"Genre: {book.genre}\n"
            details += f"Current Stock: {book.stock}\n"
            details += f"Available: {'Yes' if book.is_available() else 'No'}\n"
        
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
    
    def process_transaction(self):
        """Process transaksi berikutnya dari queue"""
        if self.library.transaction_queue.is_empty():
            messagebox.showinfo("Info", "Tidak ada transaksi untuk diproses")
            return
        
        # Get next transaction info
        next_trans = self.library.transaction_queue.peek()
        if next_trans:
            book = self.library.get_book(next_trans.book_id)
            user = self.library.users_hash.search(next_trans.user_id)
            
            msg = f"Process transaksi berikut?\n\n"
            msg += f"User: {user.username if user else 'Unknown'}\n"
            msg += f"Book: {book.title if book else 'Unknown'}\n"
            msg += f"Type: {next_trans.type}"
            
            if not messagebox.askyesno("Konfirmasi", msg):
                return
        
        success, message = self.library.process_transaction()
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_transaction_list()
            if self.on_update:
                self.on_update()
        else:
            messagebox.showerror("Error", message)
            self.refresh_transaction_list()