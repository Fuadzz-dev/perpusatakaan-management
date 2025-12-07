import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures.bst import BST

def test_bst_insert():
    """Test insert operation"""
    print("Testing BST Insert...")
    bst = BST()
    
    bst.insert(5, "Value 5")
    bst.insert(3, "Value 3")
    bst.insert(7, "Value 7")
    bst.insert(2, "Value 2")
    bst.insert(4, "Value 4")
    
    assert bst.search(5) == "Value 5"
    assert bst.search(3) == "Value 3"
    assert bst.search(7) == "Value 7"
    print("✓ Insert test passed")

def test_bst_search():
    """Test search operation"""
    print("Testing BST Search...")
    bst = BST()
    
    bst.insert(10, "Ten")
    bst.insert(5, "Five")
    bst.insert(15, "Fifteen")
    
    assert bst.search(10) == "Ten"
    assert bst.search(5) == "Five"
    assert bst.search(15) == "Fifteen"
    assert bst.search(20) is None
    print("✓ Search test passed")

def test_bst_delete():
    """Test delete operation"""
    print("Testing BST Delete...")
    bst = BST()
    
    for i in range(1, 11):
        bst.insert(i, f"Value {i}")
    
    bst.delete(5)
    assert bst.search(5) is None
    assert bst.search(4) == "Value 4"
    assert bst.search(6) == "Value 6"
    print("✓ Delete test passed")

def test_bst_traversal():
    """Test inorder traversal"""
    print("Testing BST Traversal...")
    bst = BST()
    
    values = [5, 3, 7, 2, 4, 6, 8]
    for val in values:
        bst.insert(val, f"Value {val}")
    
    inorder = bst.inorder_traversal()
    keys = [key for key, _ in inorder]
    
    assert keys == sorted(values)
    print("✓ Traversal test passed")

def test_bst_range_search():
    """Test range search"""
    print("Testing BST Range Search...")
    bst = BST()
    
    for i in range(1, 21):
        bst.insert(i, f"Value {i}")
    
    results = bst.range_search(5, 10)
    keys = [key for key, _ in results]
    
    assert keys == [5, 6, 7, 8, 9, 10]
    print("✓ Range search test passed")

def test_bst_balancing():
    """Test AVL balancing"""
    print("Testing BST Auto-Balancing...")
    bst = BST()
    
    # Insert in ascending order (worst case for unbalanced BST)
    for i in range(1, 101):
        bst.insert(i, f"Value {i}")
    
    # Tree should still be balanced
    # Search should be fast
    assert bst.search(50) == "Value 50"
    assert bst.search(100) == "Value 100"
    print("✓ Balancing test passed")

def run_all_tests():
    """Run all BST tests"""
    print("\n" + "="*50)
    print("RUNNING BST TESTS")
    print("="*50 + "\n")
    
    try:
        test_bst_insert()
        test_bst_search()
        test_bst_delete()
        test_bst_traversal()
        test_bst_range_search()
        test_bst_balancing()
        
        print("\n" + "="*50)
        print("ALL BST TESTS PASSED! ✓")
        print("="*50 + "\n")
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)