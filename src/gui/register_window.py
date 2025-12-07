import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validator import Validator

class RegisterWindow:
    """Window untuk registrasi user baru"""
    
    def __init__(self, library_system, parent_window=None):
        self.library = library_system
        self.parent_window = parent_window
        
        self.window = tk.Toplevel() if parent_window else tk.Tk()
        self.window.title("Registrasi Member Baru")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        self.create_widgets()
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.handle_register())
    
    def center_window(self):
        """Center window di layar"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Buat komponen UI"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="📝 REGISTRASI",
            font=("Arial", 24, "bold"),
            foreground="#2c3e50"
        ).pack()
        
        ttk.Label(
            header_frame,
            text="Daftar sebagai Member Perpustakaan",
            font=("Arial", 11),
            foreground="#7f8c8d"
        ).pack(pady=(5, 0))
        
        # Form frame
        form_frame = ttk.LabelFrame(main_frame, text="Data Pendaftaran", padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Username
        username_frame = ttk.Frame(form_frame)
        username_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            username_frame,
            text="Username *",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            username_frame,
            text="Minimal 3 karakter, hanya huruf, angka, dan underscore",
            font=("Arial", 8),
            foreground="gray"
        ).pack(anchor=tk.W)
        
        self.username_entry = ttk.Entry(username_frame, font=("Arial", 11), width=40)
        self.username_entry.pack(fill=tk.X, pady=(5, 0))
        self.username_entry.focus()
        
        # Password
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            password_frame,
            text="Password *",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            password_frame,
            text="Minimal 6 karakter",
            font=("Arial", 8),
            foreground="gray"
        ).pack(anchor=tk.W)
        
        self.password_entry = ttk.Entry(
            password_frame,
            font=("Arial", 11),
            show="●",
            width=40
        )
        self.password_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(
            password_frame,
            text="Tampilkan password",
            variable=self.show_password_var,
            command=self.toggle_password
        ).pack(anchor=tk.W, pady=(5, 0))
        
        # Confirm Password
        confirm_frame = ttk.Frame(form_frame)
        confirm_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            confirm_frame,
            text="Konfirmasi Password *",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        self.confirm_entry = ttk.Entry(
            confirm_frame,
            font=("Arial", 11),
            show="●",
            width=40
        )
        self.confirm_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Password strength indicator
        self.strength_label = ttk.Label(
            form_frame,
            text="",
            font=("Arial", 9)
        )
        self.strength_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Bind password entry untuk real-time validation
        self.password_entry.bind('<KeyRelease>', self.check_password_strength)
        
        # Info label
        info_frame = ttk.Frame(form_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(
            info_frame,
            text="ℹ️ Informasi:",
            font=("Arial", 9, "bold")
        ).pack(anchor=tk.W)
        
        ttk.Label(
            info_frame,
            text="• Username harus unik\n• Password akan dienkripsi dengan aman\n• Akun akan langsung aktif setelah registrasi",
            font=("Arial", 8),
            foreground="#34495e",
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Register button
        self.register_btn = ttk.Button(
            button_frame,
            text="✓ Daftar Sekarang",
            command=self.handle_register,
            width=25
        )
        self.register_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        ttk.Button(
            button_frame,
            text="✗ Batal",
            command=self.window.destroy,
            width=25
        ).pack(side=tk.LEFT, padx=5)
        
        # Footer
        footer_label = ttk.Label(
            main_frame,
            text="Sudah punya akun? Silakan login dari halaman utama",
            font=("Arial", 9),
            foreground="gray"
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def toggle_password(self):
        """Toggle show/hide password"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
            self.confirm_entry.config(show="")
        else:
            self.password_entry.config(show="●")
            self.confirm_entry.config(show="●")
    
    def check_password_strength(self, event=None):
        """Check dan tampilkan kekuatan password"""
        password = self.password_entry.get()
        
        if not password:
            self.strength_label.config(text="", foreground="black")
            return
        
        strength = 0
        feedback = []
        
        # Length check
        if len(password) >= 6:
            strength += 1
        else:
            feedback.append("minimal 6 karakter")
        
        if len(password) >= 8:
            strength += 1
        
        # Character variety
        if any(c.isupper() for c in password):
            strength += 1
        else:
            feedback.append("tambahkan huruf besar")
        
        if any(c.islower() for c in password):
            strength += 1
        else:
            feedback.append("tambahkan huruf kecil")
        
        if any(c.isdigit() for c in password):
            strength += 1
        else:
            feedback.append("tambahkan angka")
        
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            strength += 1
            feedback.append("bagus, ada karakter khusus!")
        
        # Display strength
        if strength <= 2:
            color = "red"
            text = "❌ Lemah"
        elif strength <= 4:
            color = "orange"
            text = "⚠️ Sedang"
        else:
            color = "green"
            text = "✓ Kuat"
        
        if feedback and strength < 5:
            text += f" ({', '.join(feedback[:2])})"
        
        self.strength_label.config(text=f"Kekuatan: {text}", foreground=color)
    
    def validate_input(self):
        """Validasi semua input"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        
        # Validate username
        valid, msg = Validator.validate_username(username)
        if not valid:
            messagebox.showerror("Validasi Username", msg)
            self.username_entry.focus()
            return False
        
        # Validate password
        valid, msg = Validator.validate_password(password)
        if not valid:
            messagebox.showerror("Validasi Password", msg)
            self.password_entry.focus()
            return False
        
        # Check password confirmation
        if password != confirm:
            messagebox.showerror("Error", "Password dan konfirmasi password tidak cocok!")
            self.confirm_entry.focus()
            return False
        
        # Additional password strength warning
        if len(password) < 8:
            if not messagebox.askyesno(
                "Password Lemah",
                "Password Anda kurang dari 8 karakter. Disarankan menggunakan password yang lebih panjang.\n\nLanjutkan registrasi?"
            ):
                self.password_entry.focus()
                return False
        
        return True
    
    def handle_register(self):
        """Handle registrasi"""
        # Validate input
        if not self.validate_input():
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Disable button saat proses
        self.register_btn.config(state='disabled', text="Memproses...")
        self.window.update()
        
        try:
            # Register user
            success, message = self.library.register_user(username, password, 'member')
            
            if success:
                messagebox.showinfo(
                    "Registrasi Berhasil! 🎉",
                    f"Selamat datang, {username}!\n\n{message}\n\nAnda sekarang dapat login menggunakan akun Anda."
                )
                self.window.destroy()
            else:
                messagebox.showerror("Registrasi Gagal", message)
                self.register_btn.config(state='normal', text="✓ Daftar Sekarang")
                
                # Focus ke field yang bermasalah
                if "username" in message.lower():
                    self.username_entry.focus()
                    self.username_entry.select_range(0, tk.END)
        
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan:\n{str(e)}")
            self.register_btn.config(state='normal', text="✓ Daftar Sekarang")
    
    def run(self):
        """Jalankan window"""
        self.window.mainloop()


# Untuk testing standalone
if __name__ == "__main__":
    # Mock library untuk testing
    class MockLibrary:
        def register_user(self, username, password, role):
            print(f"Mock register: {username}, {password}, {role}")
            return True, "Registrasi berhasil (mock)"
    
    mock_lib = MockLibrary()
    app = RegisterWindow(mock_lib)
    app.run()