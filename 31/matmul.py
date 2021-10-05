class Matrix(object):
    def __init__(self, values):
        self.values = values
        self.col = len(values[0])
        self.row = len(values)

    def __repr__(self):
        return f'<Matrix values="{self.values}">'

    def __matmul__(self, other):
        if not (self.row == other.col):
            raise ValueError("Matrix A rows must match B cols")

        result = []
        a = self.values
        b = other.values
        for x1 in range(self.col):
            row = []
            for y2 in range(other.row):
                row.append(sum([a[x1][k] * b[k][y2] for k in range(self.row)]))
            result.append(row)

        return Matrix(result)

    def __rmatmul__(self, other):
        return self.__matmul__(other)

    def __imatmul__(self, other):
        if not (self.row == other.col):
            raise ValueError("Matrix A rows must match B cols")

        result = self.__matmul__(other)
        self.values, self.row, self.col = result.values, result.row, result.col
        return self
