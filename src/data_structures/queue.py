class QueueNode:
    """Node untuk Queue"""
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    """Queue implementation untuk sistem transaksi (FIFO)"""
    
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def enqueue(self, data):
        """Tambah data ke belakang queue"""
        new_node = QueueNode(data)
        
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        
        self.size += 1
    
    def dequeue(self):
        """Ambil dan hapus data dari depan queue"""
        if self.is_empty():
            return None
        
        data = self.front.data
        self.front = self.front.next
        
        if self.front is None:
            self.rear = None
        
        self.size -= 1
        return data
    
    def peek(self):
        """Lihat data di depan tanpa menghapus"""
        if self.is_empty():
            return None
        return self.front.data
    
    def is_empty(self):
        """Cek apakah queue kosong"""
        return self.front is None
    
    def get_size(self):
        """Dapatkan ukuran queue"""
        return self.size
    
    def get_all(self):
        """Dapatkan semua data dalam queue"""
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def clear(self):
        """Kosongkan queue"""
        self.front = None
        self.rear = None
        self.size = 0
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        return str(self.get_all())