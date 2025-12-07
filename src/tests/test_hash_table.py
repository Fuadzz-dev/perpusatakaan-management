import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures.hash_table import HashTable

def test_hash_insert():
    """Test insert operation"""
    print("Testing Hash Table Insert...")
    ht = HashTable(10)
    
    ht.insert("key1", "value1")
    ht.insert("key2", "value2")
    ht.insert("key3", "value3")
    
    assert ht.search("key1") == "value1"
    assert ht.search("key2") == "value2"
    assert len(ht) == 3
    print("✓ Insert test passed")

def test_hash_search():
    """Test search operation"""
    print("Testing Hash Table Search...")
    ht = HashTable(10)
    
    ht.insert(1, "One")
    ht.insert(2, "Two")
    ht.insert(3, "Three")
    
    assert ht.search(1) == "One"
    assert ht.search(2) == "Two"
    assert ht.search(3) == "Three"
    assert ht.search(4) is None
    print("✓ Search test passed")

def test_hash_update():
    """Test update operation"""
    print("Testing Hash Table Update...")
    ht = HashTable(10)
    
    ht.insert("name", "John")
    assert ht.search("name") == "John"
    
    ht.insert("name", "Jane")
    assert ht.search("name") == "Jane"
    assert len(ht) == 1
    print("✓ Update test passed")

def test_hash_delete():
    """Test delete operation"""
    print("Testing Hash Table Delete...")
    ht = HashTable(10)
    
    ht.insert("a", 1)
    ht.insert("b", 2)
    ht.insert("c", 3)
    
    assert ht.delete("b") == True
    assert ht.search("b") is None
    assert ht.search("a") == 1
    assert len(ht) == 2
    print("✓ Delete test passed")

def test_hash_collision():
    """Test collision handling"""
    print("Testing Hash Table Collision Handling...")
    ht = HashTable(5)  # Small size to force collisions
    
    for i in range(20):
        ht.insert(i, f"Value {i}")
    
    for i in range(20):
        assert ht.search(i) == f"Value {i}"
    
    assert len(ht) == 20
    print("✓ Collision handling test passed")

def test_hash_rehashing():
    """Test automatic rehashing"""
    print("Testing Hash Table Rehashing...")
    ht = HashTable(10)
    
    # Insert enough items to trigger rehash
    for i in range(100):
        ht.insert(i, f"Value {i}")
    
    # All items should still be accessible
    for i in range(100):
        assert ht.search(i) == f"Value {i}"
    
    print("✓ Rehashing test passed")

def test_hash_methods():
    """Test utility methods"""
    print("Testing Hash Table Utility Methods...")
    ht = HashTable(10)
    
    ht.insert("a", 1)
    ht.insert("b", 2)
    ht.insert("c", 3)
    
    assert ht.contains("a") == True
    assert ht.contains("d") == False
    
    keys = ht.keys()
    assert "a" in keys
    assert "b" in keys
    assert "c" in keys
    
    values = ht.values()
    assert 1 in values
    assert 2 in values
    assert 3 in values
    
    print("✓ Utility methods test passed")

def run_all_tests():
    """Run all Hash Table tests"""
    print("\n" + "="*50)
    print("RUNNING HASH TABLE TESTS")
    print("="*50 + "\n")
    
    try:
        test_hash_insert()
        test_hash_search()
        test_hash_update()
        test_hash_delete()
        test_hash_collision()
        test_hash_rehashing()
        test_hash_methods()
        
        print("\n" + "="*50)
        print("ALL HASH TABLE TESTS PASSED! ✓")
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