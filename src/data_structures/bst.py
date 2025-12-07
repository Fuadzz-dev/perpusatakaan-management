class Node:
    """Node untuk Binary Search Tree"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class BST:
    """Binary Search Tree dengan AVL balancing untuk pencarian efisien"""
    
    def __init__(self):
        self.root = None
    
    def _get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        return x
    
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y
    
    def insert(self, key, value):
        """Insert node dengan auto-balancing"""
        self.root = self._insert_recursive(self.root, key, value)
    
    def _insert_recursive(self, node, key, value):
        if not node:
            return Node(key, value)
        
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        else:
            node.value = value
            return node
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)
        
        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        
        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        
        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def search(self, key):
        """Cari node berdasarkan key"""
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node, key):
        if not node or node.key == key:
            return node.value if node else None
        
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)
    
    def delete(self, key):
        """Hapus node berdasarkan key"""
        self.root = self._delete_recursive(self.root, key)
    
    def _delete_recursive(self, node, key):
        if not node:
            return node
        
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.key)
        
        if not node:
            return node
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)
        
        # Rebalancing
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)
        
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)
        
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current
    
    def inorder_traversal(self):
        """Traversal inorder (sorted)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.value))
            self._inorder_recursive(node.right, result)
    
    def range_search(self, min_key, max_key):
        """Cari semua node dalam range tertentu"""
        result = []
        self._range_search_recursive(self.root, min_key, max_key, result)
        return result
    
    def _range_search_recursive(self, node, min_key, max_key, result):
        if not node:
            return
        
        if min_key < node.key:
            self._range_search_recursive(node.left, min_key, max_key, result)
        
        if min_key <= node.key <= max_key:
            result.append((node.key, node.value))
        
        if max_key > node.key:
            self._range_search_recursive(node.right, min_key, max_key, result)
    
    def get_all(self):
        """Dapatkan semua node"""
        return self.inorder_traversal()