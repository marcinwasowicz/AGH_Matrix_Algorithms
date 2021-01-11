from queue import Queue
from typing import List
from typing import Tuple

EPSILON = 1e-14


class Vertex:
    def __init__(self, id):
        self.id = id
        self.adj = {}
        self.visited = False

    def get_degree(self):
        return len(self.adj)

    def __gt__(self, other_vertex):
        return self.get_degree() > other_vertex.get_degree()

    def __getitem__(self, key):
        return self.adj.get(key, 0.0)

    def __setitem__(self, key, value):
        self.adj[key] = value
        if abs(value) <= 0:
            del self.adj[key]

    def __delitem__(self, key):
        del self.adj[key]

    def __repr__(self):
        return str(self.id + 1)


class SparseGraphFormat:
    def __init__(self, size: int, initializer: List[Tuple[int, int, any]]):
        self.vertices = [Vertex(id) for id in range(size)]
        
        for row_idx, column_idx, value in initializer:
            self.vertices[row_idx][column_idx] = value
            self.vertices[column_idx][row_idx] = value

    @classmethod
    def from_dense_format(cls, dense_format):
        initializer = []
        size = len(dense_format)
        for row_idx, row in enumerate(dense_format):
            for column_idx, value in enumerate(row):
                if abs(value) <= EPSILON:
                    continue
                
                initializer.append((row_idx, column_idx, value))

        return cls(size, initializer)

    def _bfs(self, v: Vertex, q: Queue, ordering: List[Vertex]):
        v.visited = True
        q.put(v)
        while not q.empty():
            u = q.get()
            ordering.append(u)
            neighbours = sorted([self.vertices[i] for i in u.adj.keys()])
            for n in neighbours:
                if not n.visited:
                    n.visited = True
                    q.put(n)

    def cuthil_mckee_ordering(self):
        q = Queue(0)
        ordering = []
        self.vertices.sort()

        for v in self.vertices:
            if not v.visited:
                self._bfs(v, q, ordering)

        self.vertices = ordering
        return self.vertices
