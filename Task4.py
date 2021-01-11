from math import sqrt

EPSILON = 1e-14

class SparseMatrixCOO:
    def __init__(self, size, rows, columns, values):
        self.size = size
        self.rows = rows
        self.columns = columns
        self.values = values

    def __iter__(self):
        for row, column, value in zip(self.rows, self.columns, self.values):
            yield row, column, value

    @classmethod
    def from_dense_format(cls, dense_format):
        rows = []
        columns = []
        values =[]

        for row_idx, row in enumerate(dense_format):
            for column_idx, value in enumerate(row):
                if abs(value) > EPSILON:
                    rows.append(row_idx)
                    columns.append(column_idx)
                    values.append(value)
        return cls(len(dense_format), rows, columns, values)

    @classmethod
    def from_graph_format(cls, graph_format):
        rows = []
        columns = []
        values = []

        for vertex_idx, vertex in enumerate(graph_format.graph):
            for column_idx, value in vertex.as_row.items():
                rows.append(vertex_idx)
                columns.append(column_idx)
                values.append(value)

        return cls(len(graph_format.graph), rows, columns, values)


class Vertex:
    def __init__(self):
        self.as_row = {}
        self.as_column = {}

    def __repr__(self):
        return str([self.as_row, self.as_column])


class SparseMatrixGraph:
    def __init__(self, coo_initializer: SparseMatrixCOO):
        self.graph = [Vertex() for _ in range(coo_initializer.size)]

        for row_idx, column_idx, value in coo_initializer:
            self[row_idx, column_idx] = value

    def __getitem__(self, key):
        row, column = key
        return self.graph[row].as_row.get(column, 0.0)

    def __setitem__(self, key, value):
        row, column = key
        self.graph[row].as_row[column] = value
        self.graph[column].as_column[row] = value

        if abs(value) <= EPSILON:
            del self.graph.as_row[column]
            del self.graph[column].as_column[row]

    def __repr__(self):
        return str(self.graph)

    def __iter__(self):
        for row_idx in range(len(self.graph)):
            for column_idx in range(len(self.graph)):
                yield self[row_idx, column_idx]

    def _scale_column(self, idx):
        for row_idx, _ in self.graph[idx].as_column.items():
            if row_idx <= idx:
                continue
            self[row_idx, idx] /= self[idx, idx]

    def _subtract(self, idx):
        for column_idx, _ in self.graph[idx].as_row.items():
            if column_idx <= idx:
                continue

            for row_idx, _ in self.graph[idx].as_column.items():
                if row_idx <= idx:
                   continue

                value = -self[row_idx, idx] * self[idx, column_idx]
                if abs(self[row_idx, column_idx]) <= EPSILON:
                    self[row_idx, column_idx] = value
                else:
                    self[row_idx, column_idx] += value
    
    def lu_self_storage(self):
        for idx in range(len(self.graph)):
            self._scale_column(idx)
            self._subtract(idx)

    def get_dense_format(self):
        values = list(self)
        return [values[i: i + int(sqrt(len(values)))] for i in range(0, len(values), int(sqrt(len(values))))]

    def get_coo_format(self):
        return SparseMatrixCOO.from_graph_format(self)

# example of usage  
dense = [
    [1,3,0,0,0],
    [0,4,5,0,0],
    [0,0,6,0,0],
    [2,0,0,7,0],
    [0,0,0,0,8]
]

coo = SparseMatrixCOO.from_dense_format(dense)
graph = SparseMatrixGraph(coo)
graph.lu_self_storage()
dense = graph.get_dense_format()
coo = graph.get_coo_format()

