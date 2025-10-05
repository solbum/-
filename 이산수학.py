from fractions import Fraction

def createMatrix():
    n = int(input("n 값을 입력하세요 : "))

    matrix = [[0] * n] * n
    print("행렬을 입력하시오. : ")
    for i in range(n):
        matrix[i] = list(map(int, input().split()))

    return matrix

def getMatrixMinor(matrix, i, j):
    return[
        [row[col] for col in range(len(row)) if col != j]
        for row_idx, row in enumerate(matrix) if row_idx != i
    ]

def determinant(matrix):
    matLen = len(matrix)
    result = 0
    deterNum = 0
    if matLen == 1:
        return matrix[0][0]
    elif matLen == 2:
        result = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        return result
    else:
        for i in range(matLen):
            deterNum += ((-1) ** i) * matrix[0][i] * determinant(getMatrixMinor(matrix, 0, i))

    return deterNum

def transposeMatrix(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix))]

def matrixInverse(matrix):
    detNum = determinant(matrix)
    matLen = len(matrix)

    if matLen == 1 :
        return [[1.0 / matrix[0][0]]]
    if matLen == 2 :
        return [[matrix[1][1] / detNum, -matrix[0][1] / detNum], [-matrix[1][0] / detNum, matrix[0][0] / detNum]]
    
    cofactors = []
    for i in range(matLen):
        cofactorRow = []
        for j in range(matLen):
            minor = getMatrixMinor(matrix, i, j)
            cofactorRow.append(((-1) ** (i + j)) * determinant(minor))
        cofactors.append(cofactorRow)

    adjugate = transposeMatrix(cofactors)

    for i in range(matLen):
        for j in range(matLen):
            adjugate[i][j] = adjugate[i][j] / detNum

    return adjugate

def GJInverse(matrix):
    matLen = len(matrix)

    A = [[Fraction(x) for x in row] for row in matrix]
    I = [[Fraction(int(i==j)) for j in range(matLen)] for i in range(matLen)]
    
    for i in range(matLen):
        A[i] += I[i]

    for i in range(matLen):
        if A[i][i] == 0:
            for j in range(i + 1, matLen):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
        
        pivot = A[i][i]
        A[i] = [x / pivot for x in A[i]]

        for j in range(matLen):
            if j != i:
                ratio = A[j][i]
                A[j] = [A[j][k] - ratio * A[i][k] for k in range(2 * matLen)]

    inverse = [row[matLen:] for row in A]
    return inverse

def multiply_matrices(A, B):
    n = len(A)
    result = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    return result

def is_identity(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if i == j and matrix[i][j] != 1:
                return False
            elif i != j and matrix[i][j] != 0:
                return False
    return True



if __name__ == "__main__":
    matrix = createMatrix()
    print("행렬식 : ")
    for row in matrix:
        print([str(x) for x in row])

    detNum = determinant(matrix)
    if detNum == 0 :
        print("역행렬이 존재하지 않습니다.")

    resultMatrix1 = matrixInverse(matrix)
    print("행렬식을 이용한 역행렬 : ")
    for row in resultMatrix1:
        print([str(x) for x in row])

    resultMatrix2 = GJInverse(matrix)
    print("가우스-조던 소거법을 이용한 역행렬 : ")
    for row in resultMatrix2:
        print([str(x) for x in row])

    resultMatrix2_float = [[float(x) for x in row] for row in resultMatrix2]

    if all(
        abs(resultMatrix1[i][j] - resultMatrix2_float[i][j]) < 1e-9
        for i in range(len(matrix))
        for j in range(len(matrix))
    ):
        print("두 방식의 역행렬은 같은 값을 가진다.")
    else :
        print("두 방식의 역행렬은 같은 값을 가지지 않는다.")

    print("역행렬을 검증해보겠습니다...")
    product = multiply_matrices([[Fraction(x) for x in row] for row in matrix], resultMatrix2)
    for row in product:
        print([str(x) for x in row])

    if is_identity(product):
        print("역행렬입니다.")
    else:
        print("역행렬이 아닙니다.")

    