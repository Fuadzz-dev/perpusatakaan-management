import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LoginWindow:
    """Login window untuk autentikasi user"""
    
    def __init__(self, library_system, on_login_success):
        self.library = library_system
        self.on_login_success = on_login_success
        
        self.root = tk.Tk()
        self.root.title("Login Sistem Perpustakaan")
        self.root.geometry("400x500")
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
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="SISTEM PERPUSTAKAAN",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Library Management System",
            font=("Arial", 10)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login form frame
        form_frame = ttk.LabelFrame(main_frame, text="Login", padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Username
        ttk.Label(form_frame, text="Username:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.username_entry = ttk.Entry(form_frame, font=("Arial", 11), width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password
        ttk.Label(form_frame, text="Password:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.password_entry = ttk.Entry(form_frame, font=("Arial", 11), show="*", width=30)
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Login button
        login_btn = ttk.Button(
            form_frame,
            text="Login",
            command=self.handle_login,
            width=20
        )
        login_btn.pack(pady=10)
        
        # Register frame
        register_frame = ttk.LabelFrame(main_frame, text="Belum punya akun?", padding="20")
        register_frame.pack(fill=tk.BOTH, pady=10)
        
        ttk.Label(
            register_frame,
            text="Daftar sebagai member baru",
            font=("Arial", 9)
        ).pack(pady=(0, 10))
        
        register_btn = ttk.Button(
            register_frame,
            text="Register",
            command=self.show_register_form,
            width=20
        )
        register_btn.pack()
        
        # Info
        info_label = ttk.Label(
            main_frame,
            text="Default Admin: admin / admin123\nDefault User: user / user123",
            font=("Arial", 8),
            foreground="gray"
        )
        info_label.pack(side=tk.BOTTOM, pady=10)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.handle_login())
    
    def handle_login(self):
        """Handle login action"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan password harus diisi!")
            return
        
        success, message = self.library.login(username, password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.root.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Login Gagal", message)
            self.password_entry.delete(0, tk.END)
    
    def show_register_form(self):
        """Tampilkan form register"""
        register_window = tk.Toplevel(self.root)
        register_window.title("Register - Member Baru")
        register_window.geometry("400x350")
        register_window.resizable(False, False)
        
        # Center window
        register_window.update_idletasks()
        width = register_window.winfo_width()
        height = register_window.winfo_height()
        x = (register_window.winfo_screenwidth() // 2) - (width // 2)
        y = (register_window.winfo_screenheight() // 2) - (height // 2)
        register_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Main frame
        frame = ttk.Frame(register_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(
            frame,
            text="Registrasi Member Baru",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))
        
        # Username
        ttk.Label(frame, text="Username:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        username_entry = ttk.Entry(frame, font=("Arial", 11), width=30)
        username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password
        ttk.Label(frame, text="Password:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        password_entry = ttk.Entry(frame, font=("Arial", 11), show="*", width=30)
        password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Confirm Password
        ttk.Label(frame, text="Konfirmasi Password:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        confirm_entry = ttk.Entry(frame, font=("Arial", 11), show="*", width=30)
        confirm_entry.pack(fill=tk.X, pady=(0, 20))
        
        def handle_register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            
            if not username or not password or not confirm:
                messagebox.showerror("Error", "Semua field harus diisi!")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Password tidak cocok!")
                return
            
            if len(password) < 6:
                messagebox.showerror("Error", "Password minimal 6 karakter!")
                return
            
            success, message = self.library.register_user(username, password, 'member')
            
            if success:
                messagebox.showinfo("Success", "Registrasi berhasil! Silakan login.")
                register_window.destroy()
            else:
                messagebox.showerror("Error", message)
        
        # Register button
        ttk.Button(
            frame,
            text="Daftar",
            command=handle_register,
            width=20
        ).pack(pady=10)
        
        # Cancel button
        ttk.Button(
            frame,
            text="Batal",
            command=register_window.destroy,
            width=20
        ).pack()
    
    def run(self):
        """Jalankan window"""
        self.root.mainloop()