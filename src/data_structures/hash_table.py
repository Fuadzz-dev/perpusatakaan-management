class HashTable:
    """Hash Table dengan chaining untuk collision handling"""
    
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
    
    def _hash(self, key):
        """Hash function menggunakan metode modulo"""
        if isinstance(key, int):
            return key % self.size
        return hash(key) % self.size
    
    def insert(self, key, value):
        """Insert atau update key-value pair"""
        index = self._hash(key)
        
        # Update jika key sudah ada
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        
        # Insert baru
        self.table[index].append((key, value))
        self.count += 1
        
        # Rehash jika load factor > 0.7
        if self.count / self.size > 0.7:
            self._rehash()
    
    def search(self, key):
        """Cari value berdasarkan key"""
        index = self._hash(key)
        
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        """Hapus key-value pair"""
        index = self._hash(key)
        
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index].pop(i)
                self.count -= 1
                return True
        return False
    
    def _rehash(self):
        """Rehash table jika terlalu penuh"""
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)
    
    def get_all(self):
        """Dapatkan semua key-value pairs"""
        result = []
        for bucket in self.table:
            for key, value in bucket:
                result.append((key, value))
        return result
    
    def keys(self):
        """Dapatkan semua keys"""
        return [key for key, _ in self.get_all()]
    
    def values(self):
        """Dapatkan semua values"""
        return [value for _, value in self.get_all()]
    
    def contains(self, key):
        """Cek apakah key ada"""
        return self.search(key) is not None
    
    def __len__(self):
        return self.count
    
    def __str__(self):
        return str(self.get_all())