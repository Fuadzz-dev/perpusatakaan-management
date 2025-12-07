from collections import deque, defaultdict

class Graph:
    """Graph untuk sistem rekomendasi buku"""
    
    def __init__(self):
        self.adjacency_list = defaultdict(list)
        self.weights = {}
    
    def add_vertex(self, vertex):
        """Tambah vertex (buku/user)"""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
    
    def add_edge(self, from_vertex, to_vertex, weight=1):
        """Tambah edge dengan bobot (similarity score)"""
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        
        # Directed edge dengan weight
        if to_vertex not in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].append(to_vertex)
            self.weights[(from_vertex, to_vertex)] = weight
    
    def add_undirected_edge(self, vertex1, vertex2, weight=1):
        """Tambah edge dua arah"""
        self.add_edge(vertex1, vertex2, weight)
        self.add_edge(vertex2, vertex1, weight)
    
    def get_neighbors(self, vertex):
        """Dapatkan tetangga dari vertex"""
        return self.adjacency_list.get(vertex, [])
    
    def get_weight(self, from_vertex, to_vertex):
        """Dapatkan bobot edge"""
        return self.weights.get((from_vertex, to_vertex), 0)
    
    def bfs(self, start_vertex, max_depth=3):
        """Breadth-First Search untuk rekomendasi"""
        if start_vertex not in self.adjacency_list:
            return []
        
        visited = set()
        queue = deque([(start_vertex, 0)])
        result = []
        
        while queue:
            vertex, depth = queue.popleft()
            
            if vertex in visited or depth > max_depth:
                continue
            
            visited.add(vertex)
            if vertex != start_vertex:
                result.append((vertex, depth))
            
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        
        return result
    
    def dfs(self, start_vertex, visited=None, max_depth=3, current_depth=0):
        """Depth-First Search untuk eksplorasi rekomendasi"""
        if visited is None:
            visited = set()
        
        if start_vertex in visited or current_depth > max_depth:
            return []
        
        visited.add(start_vertex)
        result = []
        
        if current_depth > 0:
            result.append((start_vertex, current_depth))
        
        for neighbor in self.adjacency_list[start_vertex]:
            result.extend(self.dfs(neighbor, visited, max_depth, current_depth + 1))
        
        return result
    
    def get_weighted_recommendations(self, vertex, top_n=5):
        """Dapatkan rekomendasi berdasarkan bobot edge"""
        if vertex not in self.adjacency_list:
            return []
        
        recommendations = []
        for neighbor in self.adjacency_list[vertex]:
            weight = self.get_weight(vertex, neighbor)
            recommendations.append((neighbor, weight))
        
        # Sort berdasarkan weight descending
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:top_n]
    
    def collaborative_filtering(self, user_id, all_books, user_history):
        """Collaborative filtering untuk rekomendasi"""
        recommendations = []
        neighbors = self.get_neighbors(user_id)
        
        book_scores = defaultdict(float)
        
        for similar_user in neighbors:
            weight = self.get_weight(user_id, similar_user)
            similar_user_books = self.get_neighbors(similar_user)
            
            for book in similar_user_books:
                if book not in user_history:
                    book_scores[book] += weight
        
        # Sort berdasarkan score
        recommendations = sorted(book_scores.items(), key=lambda x: x[1], reverse=True)
        return recommendations
    
    def content_based_filtering(self, book_id, top_n=5):
        """Content-based filtering berdasarkan similarity"""
        return self.get_weighted_recommendations(book_id, top_n)
    
    def dijkstra(self, start_vertex):
        """Dijkstra algorithm untuk finding shortest path"""
        distances = {vertex: float('infinity') for vertex in self.adjacency_list}
        distances[start_vertex] = 0
        
        unvisited = set(self.adjacency_list.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda vertex: distances[vertex])
            
            if distances[current] == float('infinity'):
                break
            
            unvisited.remove(current)
            
            for neighbor in self.adjacency_list[current]:
                weight = self.get_weight(current, neighbor)
                distance = distances[current] + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
        
        return distances
    
    def get_all_vertices(self):
        """Dapatkan semua vertices"""
        return list(self.adjacency_list.keys())
    
    def get_all_edges(self):
        """Dapatkan semua edges"""
        edges = []
        for vertex in self.adjacency_list:
            for neighbor in self.adjacency_list[vertex]:
                weight = self.get_weight(vertex, neighbor)
                edges.append((vertex, neighbor, weight))
        return edges
    
    def clear(self):
        """Kosongkan graph"""
        self.adjacency_list.clear()
        self.weights.clear()