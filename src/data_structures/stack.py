class StackNode:
    """Node untuk Stack"""
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    """Stack implementation untuk history dan undo operations (LIFO)"""
    
    def __init__(self):
        self.top = None
        self.size = 0
    
    def push(self, data):
        """Tambah data ke top stack"""
        new_node = StackNode(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
        """Ambil dan hapus data dari top stack"""
        if self.is_empty():
            return None
        
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data
    
    def peek(self):
        """Lihat data di top tanpa menghapus"""
        if self.is_empty():
            return None
        return self.top.data
    
    def is_empty(self):
        """Cek apakah stack kosong"""
        return self.top is None
    
    def get_size(self):
        """Dapatkan ukuran stack"""
        return self.size
    
    def get_all(self):
        """Dapatkan semua data dalam stack"""
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def clear(self):
        """Kosongkan stack"""
        self.top = None
        self.size = 0
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        return str(self.get_all())