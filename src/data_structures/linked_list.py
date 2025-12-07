class ListNode:
    """Node untuk Linked List"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Doubly Linked List untuk manajemen data fleksibel"""
    
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, data):
        """Tambah data di akhir list"""
        new_node = ListNode(data)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self.size += 1
    
    def prepend(self, data):
        """Tambah data di awal list"""
        new_node = ListNode(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert_at(self, index, data):
        """Insert data di posisi tertentu"""
        if index < 0 or index > self.size:
            return False
        
        if index == 0:
            self.prepend(data)
            return True
        
        new_node = ListNode(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return True
    
    def delete(self, data):
        """Hapus node dengan data tertentu"""
        if not self.head:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def delete_at(self, index):
        """Hapus node di posisi tertentu"""
        if index < 0 or index >= self.size:
            return None
        
        if index == 0:
            data = self.head.data
            self.head = self.head.next
            self.size -= 1
            return data
        
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        data = current.next.data
        current.next = current.next.next
        self.size -= 1
        return data
    
    def search(self, data):
        """Cari node dengan data tertentu"""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1
    
    def get(self, index):
        """Dapatkan data di posisi tertentu"""
        if index < 0 or index >= self.size:
            return None
        
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data
    
    def get_all(self):
        """Dapatkan semua data"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def clear(self):
        """Kosongkan list"""
        self.head = None
        self.size = 0
    
    def is_empty(self):
        """Cek apakah list kosong"""
        return self.head is None
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        return str(self.get_all())