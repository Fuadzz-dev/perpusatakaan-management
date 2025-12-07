import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.library import Library

def test_transaction_flow():
    """Test complete transaction flow"""
    print("Testing Transaction Flow...")
    
    lib = Library()
    
    # Register users
    lib.register_user("testuser", "password", "member")
    lib.register_user("testadmin", "password", "admin")
    
    # Login as member
    lib.login("testuser", "password")
    user_id = lib.current_user.user_id
    
    # Add book as admin
    lib.logout()
    lib.login("testadmin", "password")
    lib.add_book("Test Book", "Test Author", stock=5)
    book_id = lib.next_book_id - 1
    
    # Login as member and request borrow
    lib.logout()
    lib.login("testuser", "password")
    success, msg = lib.request_borrow(book_id)
    assert success == True
    
    # Check queue
    assert lib.transaction_queue.get_size() > 0
    
    # Process as admin
    lib.logout()
    lib.login("testadmin", "password")
    success, msg = lib.process_transaction()
    assert success == True
    
    # Check book stock
    book = lib.get_book(book_id)
    assert book.stock == 4
    
    print("✓ Transaction flow test passed")

def test_queue_operations():
    """Test queue for transactions"""
    print("Testing Queue Operations...")
    
    lib = Library()
    lib.register_user("admin", "pass", "admin")
    lib.login("admin", "pass")
    
    # Add books
    lib.add_book("Book 1", stock=10)
    lib.add_book("Book 2", stock=10)
    book1_id = lib.next_book_id - 2
    book2_id = lib.next_book_id - 1
    
    # Add users
    lib.register_user("user1", "pass", "member")
    lib.register_user("user2", "pass", "member")
    
    # Create transactions
    lib.logout()
    lib.login("user1", "pass")
    lib.request_borrow(book1_id)
    
    lib.logout()
    lib.login("user2", "pass")
    lib.request_borrow(book2_id)
    
    # Check FIFO order
    lib.logout()
    lib.login("admin", "pass")
    
    first_trans = lib.transaction_queue.peek()
    assert first_trans.book_id == book1_id
    
    lib.process_transaction()
    second_trans = lib.transaction_queue.peek()
    assert second_trans.book_id == book2_id
    
    print("✓ Queue operations test passed")

def test_history_stack():
    """Test history stack"""
    print("Testing History Stack...")
    
    lib = Library()
    lib.register_user("admin", "pass", "admin")
    lib.login("admin", "pass")
    
    lib.add_book("Book", stock=5)
    book_id = lib.next_book_id - 1
    
    lib.register_user("user", "pass", "member")
    lib.logout()
    lib.login("user", "pass")
    
    # Borrow
    lib.request_borrow(book_id)
    
    lib.logout()
    lib.login("admin", "pass")
    lib.process_transaction()
    
    # Check history
    assert lib.history_stack.get_size() > 0
    last_action = lib.history_stack.peek()
    assert last_action['action'] == 'borrow'
    
    print("✓ History stack test passed")

def test_stock_management():
    """Test stock management"""
    print("Testing Stock Management...")
    
    lib = Library()
    lib.register_user("admin", "pass", "admin")
    lib.login("admin", "pass")
    
    lib.add_book("Limited Book", stock=1)
    book_id = lib.next_book_id - 1
    
    lib.register_user("user1", "pass", "member")
    lib.register_user("user2", "pass", "member")
    
    # First user borrows
    lib.logout()
    lib.login("user1", "pass")
    lib.request_borrow(book_id)
    
    lib.logout()
    lib.login("admin", "pass")
    lib.process_transaction()
    
    book = lib.get_book(book_id)
    assert book.stock == 0
    assert not book.is_available()
    
    # Second user tries to borrow
    lib.logout()
    lib.login("user2", "pass")
    success, msg = lib.request_borrow(book_id)
    assert success == True  # Request accepted
    
    # But processing fails
    lib.logout()
    lib.login("admin", "pass")
    success, msg = lib.process_transaction()
    assert success == False  # Should fail due to no stock
    
    print("✓ Stock management test passed")

def run_all_tests():
    """Run all transaction tests"""
    print("\n" + "="*50)
    print("RUNNING TRANSACTION TESTS")
    print("="*50 + "\n")
    
    try:
        test_transaction_flow()
        test_queue_operations()
        test_history_stack()
        test_stock_management()
        
        print("\n" + "="*50)
        print("ALL TRANSACTION TESTS PASSED! ✓")
        print("="*50 + "\n")
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)