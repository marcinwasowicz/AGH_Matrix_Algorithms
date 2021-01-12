from queue import Queue
from typing import List
from typing import Tuple
from math import sqrt

import random

EPSILON = 1e-14


class Vertex:
    def __init__(self, id):
        self.id = id
        self.as_row = {}
        self.as_column = {}
        self.visited = False

    def get_degree(self):
        return len(self.as_column) + len(self.as_row)

    def __gt__(self, other_vertex):
        return self.get_degree() > other_vertex.get_degree()

    def __repr__(self):
        return str(self.id + 1)


class SparseGraphFormat:
    def __init__(self, size: int, initializer: List[Tuple[int, int, any]]):
        self.vertices = [Vertex(id) for id in range(size)]
        
        for row_idx, column_idx, value in initializer:
            self.vertices[row_idx].as_row[column_idx] = value
            self.vertices[column_idx].as_column[row_idx] = value

    def __repr__(self):
        return str([[vertex.as_row.get(i, 0.0) for i in range(len(self.vertices))] for vertex in self.vertices])

    def __getitem__(self, key):
        row_idx, column_idx = key
        return self.vertices[row_idx].as_row.get(column_idx, 0.0)

    def __setitem__(self, key, value):
        row_idx, column_idx = key
        self.vertices[row_idx].as_row[column_idx] = value
        self.vertices[column_idx].as_column[row_idx] = value

    def __delitem__(self, key):
        row_idx, column_idx = key
        del self.vertices[row_idx].as_row[column_idx] 
        del self.vertices[column_idx].as_column[row_idx] 

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
            neighbours = sorted([self.vertices[i] for i in u.as_row])
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

        mapping = {v.id: i for i, v in enumerate(ordering)}

        reordered_vertices = [Vertex(i) for i in range(len(self.vertices))]

        for vertex in self.vertices:
            reordered_vertices[mapping[vertex.id]].as_row = {mapping[key]: value for key, value in vertex.as_row.items()}
            reordered_vertices[mapping[vertex.id]].as_column = {mapping[key]: value for key, value in vertex.as_column.items()}

        self.vertices = reordered_vertices


    def lu_self_storage(self):
        fill_in_count = 0

        for idx in range(len(self.vertices)):
            for row_idx, _ in self.vertices[idx].as_column.items():
                if row_idx <= idx:
                    continue
                self[row_idx, idx] /= self[idx, idx]

            for column_idx, _ in self.vertices[idx].as_row.items():
                if column_idx <= idx:
                    continue

                for row_idx, _ in self.vertices[idx].as_column.items():
                    if row_idx <= idx:
                        continue

                    value = -self[row_idx, idx] * self[idx, column_idx]
                    if abs(self[row_idx, column_idx]) <= EPSILON:
                        fill_in_count += 1
                        self[row_idx, column_idx] = value
                    else:
                        self[row_idx, column_idx] += value
                    if abs(self[row_idx, column_idx]) <= EPSILON:
                        fill_in_count -= 1
                        del self[row_idx, column_idx]

        return fill_in_count


def generate_test(size, non_zero_count):
    assert size <= non_zero_count
    idxs = [idx for idx in range(size)]
    initializer = []

    for idx in idxs:
        initializer.append((idx, idx, random.uniform(1, 100)))

    for _ in range(non_zero_count - size):
        initializer.append((
            random.choice(idxs),
            random.choice(idxs),
            random.uniform(1, 100)
        ))

    sparse1 = SparseGraphFormat(size, initializer)
    sparse2 = SparseGraphFormat(size, initializer)

    sparse1.cuthil_mckee_ordering()

    return sparse1.lu_self_storage(), sparse2.lu_self_storage()


def run_tests():
    test_count = 0
    passed_count = 0

    for size in range(100, 1001):
        for nnz in [2*size, 3*size, 4*size, 5*size]:

            test_count += 1

            ordered, non_ordered = generate_test(size, nnz)

            if ordered > non_ordered:
                passed_count += 1

    return passed_count/test_count

print(run_tests())
