import numpy

EPSILON=1*10e-4

def create_matrix(size:int):
    """Функція що створює матрицю необхідного розміру а також вектор b"""
    matrix = [[0]*n for i in range(n)]
    b = list(x for x in range(1,n+1))
    for i in range(n):
        matrix[i][i] = 3
        if i<n-1:
            matrix[i][i+1]=2
        if i!=0:
            matrix[i][i-1]=1

    return matrix,b


def check_first_condition(matrix:numpy.ndarray,size:int):
    for i in range(size):
        sum_of_another_elements_in_row = 0
        for j in range(n):
            if j!=i:
                sum_of_another_elements_in_row+=abs(matrix[i][j])
        if abs(matrix[i][i]<sum_of_another_elements_in_row):
            return False
    return True
        

def check_second_condition(matrix:numpy.ndarray,transposed_matrix:numpy.ndarray,size:int):
    if not (matrix==transposed_matrix).all():
        return False
    
    if numpy.linalg.det(matrix)<=0:
        return False

    matrix_with_deleted_row =numpy.delete(matrix,size-1,axis=0)
    matrix_with_deleted_column = numpy.delete(matrix_with_deleted_row,size-1,axis=1)

    if numpy.linalg.det(matrix_with_deleted_column)<=0:
        return False

    for i in range(size-2,0,-1):
        matrix_with_deleted_row = numpy.delete(matrix_with_deleted_column,i,axis=0)
        matrix_with_deleted_column = numpy.delete(matrix_with_deleted_row,i,axis=1)
        if numpy.linalg.det(matrix_with_deleted_column)<=0:
            return False
    
    return True


def evaluate_xi(matrix:numpy.ndarray,x_vector:list[float],b:list[int],i:int,size:int,x_old_version):
    first_sum = 0
    second_sum = 0
    for j in range(1,i+1):
        first_sum+= (matrix[i][j-1]*x_vector[j-1])/matrix[i][i]
    
    for j in range(i+1,size):
        second_sum += (matrix[i][j]*x_old_version[j])/matrix[i][i]

    x_vector[i] = -first_sum-second_sum+b[i]/matrix[i][i]


def iterations(matrix,x_vector,x_old_version,b,n,number_of_iterations):
    for i in range(n):
        evaluate_xi(matrix,x_vector,b,i,n,x_old_version)
    
    x_difference:list[float] = [abs(x_vector[i]-x_old_version[i]) for i in range(n)]

    if max(x_difference)<EPSILON:
        return False
    
    print(f"Iteration №{number_of_iteration}:{x_vector}")
    print("\n\n\n")
    
    for i in range(n):
        x_old_version[i]=x_vector[i]
    return True


if __name__=="__main__":
        n=10
        
        matrix,b=create_matrix(n)
        matrix = numpy.array(matrix)
        transposed_matrix=numpy.transpose(matrix)
        
        if not (check_first_condition(matrix,n) or check_second_condition(matrix,transposed_matrix,n)):
            raise Exception("Both of conditions of convergence are not fullfilled")

        x_vector:list[float]=[0 for _ in range(n)]
        
        x_old_version = [0 for _ in range(n)]

        number_of_iteration=1
        while iterations(matrix,x_vector,x_old_version,b,n,number_of_iteration):
            number_of_iteration+=1

        print(x_vector)
        
        
        

    
    
    