import json
import os
from datetime import datetime

class FileHandler:
    """Handler untuk persistensi data ke file JSON"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Pastikan directory data ada"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_json(self, filename, data):
        """Simpan data ke file JSON"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True, f"Data berhasil disimpan ke {filename}"
        except Exception as e:
            return False, f"Gagal menyimpan data: {str(e)}"
    
    def load_json(self, filename, default=None):
        """Load data dari file JSON"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            return default if default is not None else []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
            return default if default is not None else []
    
    def delete_file(self, filename):
        """Hapus file"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True, f"File {filename} berhasil dihapus"
            return False, f"File {filename} tidak ditemukan"
        except Exception as e:
            return False, f"Gagal menghapus file: {str(e)}"
    
    def backup_data(self, filename):
        """Buat backup file"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            return False, f"File {filename} tidak ditemukan"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{filename}.backup_{timestamp}"
        backup_filepath = os.path.join(self.data_dir, backup_filename)
        
        try:
            data = self.load_json(filename)
            with open(backup_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True, f"Backup berhasil: {backup_filename}"
        except Exception as e:
            return False, f"Gagal membuat backup: {str(e)}"
    
    def list_files(self, extension='.json'):
        """List semua file dengan ekstensi tertentu"""
        try:
            files = [f for f in os.listdir(self.data_dir) if f.endswith(extension)]
            return files
        except Exception as e:
            print(f"Error listing files: {str(e)}")
            return []
    
    def file_exists(self, filename):
        """Cek apakah file ada"""
        filepath = os.path.join(self.data_dir, filename)
        return os.path.exists(filepath)
    
    def get_file_size(self, filename):
        """Dapatkan ukuran file dalam bytes"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            return os.path.getsize(filepath)
        except:
            return 0
    
    def export_to_csv(self, filename, data, headers):
        """Export data ke CSV"""
        import csv
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            return True, f"Data berhasil diexport ke {filename}"
        except Exception as e:
            return False, f"Gagal export data: {str(e)}"