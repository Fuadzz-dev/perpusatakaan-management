import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.register_window import RegisterWindow

class LoginWindow:
    """Login window untuk autentikasi user"""
    
    def __init__(self, library_system, on_login_success):
        self.library = library_system
        self.on_login_success = on_login_success
        
        self.root = tk.Tk()
        self.root.title("Login Sistem Perpustakaan")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        self.create_widgets()
    
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
        # Main frame
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with icon
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header_frame,
            text="📚",
            font=("Arial", 40)
        ).pack()
        
        ttk.Label(
            header_frame,
            text="SISTEM PERPUSTAKAAN",
            font=("Arial", 20, "bold"),
            foreground="#2c3e50"
        ).pack(pady=(5, 0))
        
        ttk.Label(
            header_frame,
            text="Library Management System",
            font=("Arial", 10),
            foreground="#7f8c8d"
        ).pack()
        
        # Login form frame
        form_frame = ttk.LabelFrame(main_frame, text="Login", padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # Username
        ttk.Label(
            form_frame,
            text="Username:",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.username_entry = ttk.Entry(form_frame, font=("Arial", 11), width=35)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        self.username_entry.focus()
        
        # Password
        ttk.Label(
            form_frame,
            text="Password:",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))
        
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.password_entry = ttk.Entry(
            password_frame,
            font=("Arial", 11),
            show="●",
            width=15
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(
            password_frame,
            text="Tampilkan password",
            variable=self.show_password_var,
            command=self.toggle_password
        ).pack(anchor=tk.W)
        
        # Login button
        self.login_btn = ttk.Button(
            form_frame,
            text="🔐 Login",
            command=self.handle_login,
            width=25
        )
        self.login_btn.pack(pady=15)
        
        # Register section
        register_frame = ttk.LabelFrame(
            main_frame,
            text="Belum punya akun?",
            padding="20"
        )
        register_frame.pack(fill=tk.X, pady=10)
        
        self.register_btn = ttk.Button(
            register_frame,
            text="📝 Daftar Sekarang",
            command=self.show_register_form,
            width=30
        )
        self.register_btn.pack(pady=8)


        
        # Info credentials
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(side=tk.BOTTOM)
        
        # ttk.Label(
        #     info_frame,
        #     text="Akun Demo:",
        #     font=("Arial", 8, "bold"),
        #     foreground="gray"
        # ).pack()
        
        # ttk.Label(
        #     info_frame,
        #     text="Admin: admin / admin123\nMember: user / user123",
        #     font=("Arial", 8),
        #     foreground="gray",
        #     justify=tk.CENTER
        # ).pack()
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.handle_login())
    
    def toggle_password(self):
        """Toggle show/hide password"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
    
    def handle_login(self):
        """Handle login action"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan password harus diisi!")
            return
        
        # Disable button saat proses
        self.login_btn.config(state='disabled', text="Memproses...")
        self.root.update()
        
        try:
            success, message = self.library.login(username, password)
            
            if success:
                messagebox.showinfo("Login Berhasil", f"Selamat datang!\n\n{message}")
                self.root.destroy()
                self.on_login_success()
            else:
                messagebox.showerror("Login Gagal", message)
                self.password_entry.delete(0, tk.END)
                self.login_btn.config(state='normal', text="🔐 Login")
                self.password_entry.focus()
        
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan:\n{str(e)}")
            self.login_btn.config(state='normal', text="🔐 Login")
    
    def show_register_form(self):
        """Tampilkan form register"""
        try:
            RegisterWindow(self.library, self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka form registrasi:\n{str(e)}")
    
    def run(self):
        """Jalankan window"""
        self.root.mainloop()