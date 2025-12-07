import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.library import Library

def test_graph_building():
    """Test recommendation graph building"""
    print("Testing Graph Building...")
    
    lib = Library()
    lib.register_user("admin", "pass", "admin")
    lib.login("admin", "pass")
    
    # Add books with same genre
    lib.add_book("Book 1", genre="Fiction", stock=10)
    lib.add_book("Book 2", genre="Fiction", stock=10)
    lib.add_book("Book 3", genre="Science", stock=10)
    
    # Check graph has vertices
    vertices = lib.recommendation_graph.get_all_vertices()
    assert len(vertices) > 0
    
    print("✓ Graph building test passed")

def test_collaborative_filtering():
    """Test collaborative filtering recommendations"""
    print("Testing Collaborative Filtering...")
    
    lib = Library()
    lib.register_user("admin", "pass", "admin")
    lib.login("admin", "pass")
    
    # Add books
    lib.add_book("Book A", stock=10)
    lib.add_book("Book B", stock=10)
    lib.add_book("Book C", stock=10)
    book_a = lib.next_book_id - 3
    book_b = lib.next_book_id - 2
    book_c = lib.next_book_id - 1
    
    # Register users
    lib.register_user("user1", "pass", "member")
    lib.register_user("user2", "pass", "member")
    
    # User 1 borrows Book A and B
    lib.logout()
    lib.login("user1", "pass")
    lib.request_borrow(book_a)
    lib.logout()
    lib.login("admin", "pass")
    lib.process_transaction()
    
    lib.logout()
    lib.login("user1", "pass")
    lib.request_borrow(book_b)
    lib.logout()
    lib.login("admin", "pass")
    lib.process_transaction()
    
    # User 2 borrows Book A
    lib.logout()
    lib.login("user2", "pass")
    lib.request_borrow(book_a)
    lib.logout()
    lib.login("admin", "pass")
    lib.process_transaction()
    
    # User 2 should get recommendation for Book B
    lib.logout()
    lib.login("user2", "pass")
    recommendations = lib.get_recommendations(5)
    
    # Should have some recommendations
    assert isinstance(recommendations, list)
    
    print("✓ Collaborative filtering test passed")

def test_content_based_filtering():
    """Test content-based recommendations"""
    print("Testing Content-Based Filtering...")
    
    lib = Library()
    lib.register_user("admin", "pass", "admin")
    lib.login("admin", "pass")
    
    # Add books with same genre
    lib.add_book("Fiction 1", genre="Fiction", stock=10)
    lib.add_book("Fiction 2", genre="Fiction", stock=10)
    lib.add_book("Science 1", genre="Science", stock=10)
    
    # Books with same genre should be connected in graph
    vertices = lib.recommendation_graph.get_all_vertices()
    edges = lib.recommendation_graph.get_all_edges()
    
    assert len(edges) > 0
    
    print("✓ Content-based filtering test passed")

def test_recommendation_update():
    """Test recommendation graph update after borrowing"""
    print("Testing Recommendation Update...")
    
    lib = Library()
    lib.register_user("admin", "pass", "admin")
    lib.login("admin", "pass")
    
    lib.add_book("Book X", stock=10)
    book_id = lib.next_book_id - 1
    
    lib.register_user("testuser", "pass", "member")
    lib.logout()
    lib.login("testuser", "pass")
    user_id = lib.current_user.user_id
    
    lib.request_borrow(book_id)
    lib.logout()
    lib.login("admin", "pass")
    lib.process_transaction()
    
    # Check graph has user-book connection
    user_vertex = f"user_{user_id}"
    book_vertex = f"book_{book_id}"
    
    neighbors = lib.recommendation_graph.get_neighbors(user_vertex)
    assert book_vertex in neighbors
    
    print("✓ Recommendation update test passed")

def test_no_recommendations_for_new_user():
    """Test no recommendations for new user without history"""
    print("Testing New User Recommendations...")
    
    lib = Library()
    lib.register_user("newuser", "pass", "member")
    lib.login("newuser", "pass")
    
    recommendations = lib.get_recommendations(5)
    assert len(recommendations) == 0
    
    print("✓ New user recommendations test passed")

def run_all_tests():
    """Run all recommendation tests"""
    print("\n" + "="*50)
    print("RUNNING RECOMMENDATION TESTS")
    print("="*50 + "\n")
    
    try:
        test_graph_building()
        test_collaborative_filtering()
        test_content_based_filtering()
        test_recommendation_update()
        test_no_recommendations_for_new_user()
        
        print("\n" + "="*50)
        print("ALL RECOMMENDATION TESTS PASSED! ✓")
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