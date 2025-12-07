import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validator import Validator

class BookManagementWindow:
    """Window untuk manajemen buku (admin only)"""
    
    def __init__(self, library_system, on_update_callback=None):
        self.library = library_system
        self.on_update = on_update_callback
        
        if not self.library.is_admin():
            messagebox.showerror("Error", "Hanya admin yang dapat mengakses fitur ini!")
            return
        
        self.window = tk.Toplevel()
        self.window.title("Manajemen Buku")
        self.window.geometry("900x600")
        
        self.create_widgets()
        self.refresh_book_list()
    
    def create_widgets(self):
        """Buat komponen UI"""
        # Title
        ttk.Label(
            self.window,
            text="Manajemen Buku",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Main container
        main_container = ttk.Frame(self.window)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Book list
        left_panel = ttk.LabelFrame(main_container, text="Daftar Buku", padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Treeview
        tree_frame = ttk.Frame(left_panel)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Title", "Author", "Stock")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        
        self.tree.column("Title", width=200)
        self.tree.column("Author", width=150)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_book_select)
        
        # Right panel - Form
        right_panel = ttk.LabelFrame(main_container, text="Form Buku", padding="10")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 0))
        
        # Form fields
        fields = [
            ("ID:", "id_var"),
            ("Judul:", "title_var"),
            ("Penulis:", "author_var"),
            ("ISBN:", "isbn_var"),
            ("Genre:", "genre_var"),
            ("Tahun:", "year_var"),
            ("Stock:", "stock_var"),
            ("Deskripsi:", "desc_var")
        ]
        
        self.form_vars = {}
        
        for label, var_name in fields:
            ttk.Label(right_panel, text=label).pack(anchor=tk.W, pady=(5, 0))
            
            if var_name == "desc_var":
                text_widget = tk.Text(right_panel, height=4, width=30)
                text_widget.pack(fill=tk.X, pady=(0, 10))
                self.form_vars[var_name] = text_widget
            else:
                var = tk.StringVar()
                entry = ttk.Entry(right_panel, textvariable=var, width=30)
                entry.pack(fill=tk.X, pady=(0, 10))
                self.form_vars[var_name] = var
                
                if var_name == "id_var":
                    entry.config(state='readonly')
        
        # Buttons
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="Tambah Baru",
            command=self.add_book
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame,
            text="Update",
            command=self.update_book
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame,
            text="Hapus",
            command=self.delete_book
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form
        ).pack(fill=tk.X, pady=2)
    
    def refresh_book_list(self):
        """Refresh daftar buku"""
        self.tree.delete(*self.tree.get_children())
        
        books = self.library.get_all_books()
        for book in books:
            self.tree.insert('', tk.END, values=(
                book.books_id,
                book.title,
                book.author,
                book.stock
            ))
    
    def on_book_select(self, event):
        """Handle pemilihan buku dari tree"""
        selection = self.tree.selection()
        if not selection:
            return
        
        values = self.tree.item(selection[0])['values']
        book_id = values[0]
        
        book = self.library.get_book(book_id)
        if book:
            self.form_vars['id_var'].set(book.books_id)
            self.form_vars['title_var'].set(book.title)
            self.form_vars['author_var'].set(book.author)
            self.form_vars['isbn_var'].set(book.isbn)
            self.form_vars['genre_var'].set(book.genre)
            self.form_vars['year_var'].set(book.year or "")
            self.form_vars['stock_var'].set(book.stock)
            
            desc_widget = self.form_vars['desc_var']
            desc_widget.delete(1.0, tk.END)
            desc_widget.insert(1.0, book.description)
    
    def clear_form(self):
        """Bersihkan form"""
        self.form_vars['id_var'].set("")
        self.form_vars['title_var'].set("")
        self.form_vars['author_var'].set("")
        self.form_vars['isbn_var'].set("")
        self.form_vars['genre_var'].set("")
        self.form_vars['year_var'].set("")
        self.form_vars['stock_var'].set("")
        
        desc_widget = self.form_vars['desc_var']
        desc_widget.delete(1.0, tk.END)
    
    def add_book(self):
        """Tambah buku baru"""
        title = self.form_vars['title_var'].get().strip()
        author = self.form_vars['author_var'].get().strip()
        isbn = self.form_vars['isbn_var'].get().strip()
        genre = self.form_vars['genre_var'].get().strip()
        year = self.form_vars['year_var'].get().strip()
        stock = self.form_vars['stock_var'].get().strip()
        desc_widget = self.form_vars['desc_var']
        description = desc_widget.get(1.0, tk.END).strip()
        
        # Validasi
        valid, msg = Validator.validate_book_title(title)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        if stock:
            valid, msg = Validator.validate_stock(stock)
            if not valid:
                messagebox.showerror("Error", msg)
                return
            stock = int(stock)
        else:
            stock = 1
        
        if year:
            valid, msg = Validator.validate_year(year)
            if not valid:
                messagebox.showerror("Error", msg)
                return
            year = int(year)
        else:
            year = None
        
        success, message = self.library.add_book(
            title=title,
            author=author,
            isbn=isbn,
            genre=genre,
            year=year,
            stock=stock,
            description=description
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_book_list()
            self.clear_form()
            if self.on_update:
                self.on_update()
        else:
            messagebox.showerror("Error", message)
    
    def update_book(self):
        """Update buku yang dipilih"""
        book_id = self.form_vars['id_var'].get()
        
        if not book_id:
            messagebox.showwarning("Warning", "Pilih buku terlebih dahulu!")
            return
        
        book_id = int(book_id)
        
        title = self.form_vars['title_var'].get().strip()
        author = self.form_vars['author_var'].get().strip()
        isbn = self.form_vars['isbn_var'].get().strip()
        genre = self.form_vars['genre_var'].get().strip()
        year = self.form_vars['year_var'].get().strip()
        stock = self.form_vars['stock_var'].get().strip()
        desc_widget = self.form_vars['desc_var']
        description = desc_widget.get(1.0, tk.END).strip()
        
        # Validasi
        valid, msg = Validator.validate_book_title(title)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        if stock:
            valid, msg = Validator.validate_stock(stock)
            if not valid:
                messagebox.showerror("Error", msg)
                return
            stock = int(stock)
        
        if year:
            valid, msg = Validator.validate_year(year)
            if not valid:
                messagebox.showerror("Error", msg)
                return
            year = int(year)
        else:
            year = None
        
        success, message = self.library.update_book(
            book_id=book_id,
            title=title,
            author=author,
            isbn=isbn,
            genre=genre,
            year=year,
            stock=stock,
            description=description
        )
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_book_list()
            if self.on_update:
                self.on_update()
        else:
            messagebox.showerror("Error", message)
    
    def delete_book(self):
        """Hapus buku yang dipilih"""
        book_id = self.form_vars['id_var'].get()
        
        if not book_id:
            messagebox.showwarning("Warning", "Pilih buku terlebih dahulu!")
            return
        
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus buku ini?"):
            return
        
        book_id = int(book_id)
        
        success, message = self.library.delete_book(book_id)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_book_list()
            self.clear_form()
            if self.on_update:
                self.on_update()
        else:
            messagebox.showerror("Error", message)