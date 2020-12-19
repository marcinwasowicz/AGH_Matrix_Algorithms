EPSILON = 1e-14

class Vertex:
    def __init__(self):
        self.as_row = {}
        self.as_column = {}

    def __repr__(self):
        return str([self.as_row, self.as_column])

class SparseMatrixGraph:
    def __init__(self, dense_initializer):
        self.graph = [Vertex() for _ in dense_initializer]

        for row_idx, row in enumerate(dense_initializer):
            for column_idx, value in enumerate(row):
                if abs(value) > EPSILON:
                    self[row_idx, column_idx] = value

    def __getitem__(self, key):
        row, column = key
        return self.graph[row].as_row.get(column, 0.0)

    def __setitem__(self, key, value):
        row, column = key
        self.graph[row].as_row[column] = value
        self.graph[column].as_column[row] = value

    def __repr__(self):
        return str(self.graph)

    def __iter__(self):
        for row_idx in range(len(self.graph)):
            for column_idx in range(len(self.graph)):
                yield self[row_idx, column_idx]
        
    def lu_self_storage(self):
        for idx in range(len(self.graph)):
            for row_idx, _ in self.graph[idx].as_column.items():
                if row_idx <= idx:
                    continue
                self[row_idx, idx] /= self[idx, idx]

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

