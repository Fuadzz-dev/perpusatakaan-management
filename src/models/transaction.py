from datetime import datetime

class Transaction:
    """Model untuk transaksi peminjaman/pengembalian"""
    
    def __init__(self, transaction_id, user_id, book_id, trans_type, 
                 status='pending', timestamp=None):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.book_id = book_id
        self.type = trans_type  # 'borrow' atau 'return'
        self.status = status    # 'pending', 'approved', 'rejected'
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()
    
    def to_dict(self):
        """Convert ke dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'type': self.type,
            'status': self.status,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data):
        """Create Transaction dari dictionary"""
        return Transaction(
            transaction_id=data.get('transaction_id'),
            user_id=data.get('user_id'),
            book_id=data.get('book_id'),
            trans_type=data.get('type', 'borrow'),
            status=data.get('status', 'pending'),
            timestamp=data.get('timestamp')
        )
    
    def is_pending(self):
        """Cek apakah transaksi masih pending"""
        return self.status == 'pending'
    
    def approve(self):
        """Approve transaksi"""
        self.status = 'approved'
    
    def reject(self):
        """Reject transaksi"""
        self.status = 'rejected'
    
    def is_borrow(self):
        """Cek apakah transaksi peminjaman"""
        return self.type == 'borrow'
    
    def is_return(self):
        """Cek apakah transaksi pengembalian"""
        return self.type == 'return'
    
    def __str__(self):
        return f"Transaction {self.transaction_id}: {self.type} - {self.status}"
    
    def __repr__(self):
        return f"Transaction(id={self.transaction_id}, type='{self.type}', status='{self.status}')"

class BorrowHistory:
    """Model untuk history peminjaman"""
    
    def __init__(self, history_id, user_id, book_id, borrow_date=None, return_date=None):
        self.history_id = history_id
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = borrow_date if borrow_date else datetime.now().isoformat()
        self.return_date = return_date
    
    def to_dict(self):
        """Convert ke dictionary"""
        return {
            'history_id': self.history_id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'borrow_date': self.borrow_date,
            'return_date': self.return_date
        }
    
    @staticmethod
    def from_dict(data):
        """Create BorrowHistory dari dictionary"""
        return BorrowHistory(
            history_id=data.get('history_id'),
            user_id=data.get('user_id'),
            book_id=data.get('book_id'),
            borrow_date=data.get('borrow_date'),
            return_date=data.get('return_date')
        )
    
    def is_returned(self):
        """Cek apakah sudah dikembalikan"""
        return self.return_date is not None
    
    def mark_returned(self):
        """Tandai sebagai sudah dikembalikan"""
        self.return_date = datetime.now().isoformat()
    
    def __str__(self):
        status = "Returned" if self.is_returned() else "Borrowed"
        return f"History {self.history_id}: {status}"