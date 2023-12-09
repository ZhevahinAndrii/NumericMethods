import numpy

def create_matrix(size:int):
    """Функція що створює матрицю необхідного розміру а також вектор f,попередньо замінивши всі знаки в початковому векторі вільних членів на протилежний"""
    matrix = [[0]*n for i in range(n)]
    f = list(-x for x in range(1,n+1))
    for i in range(n):
        matrix[i][i] = 3
        if i<n-1:
            matrix[i][i+1]=2
        if i!=0:
            matrix[i][i-1]=1

    return matrix,f

def inverse_matrix_gauss(matrix):
    # Перевірка, чи матриця квадратна
    rows, cols = matrix.shape
    if rows != cols:
        raise ValueError("Матриця повинна бути квадратною для обчислення оберненої матриці.")

    # Створення розширеної матриці [matrix | I]
    augmented_matrix = numpy.hstack([matrix,numpy.identity(len(matrix))])
    # Приведення матриці до ступеневої форми
    for i in range(rows):
        # Нормалізація рядка
        pivot = augmented_matrix[i, i]
        augmented_matrix[i, :] /= pivot
        
        # factora = augmented_matrix[i+1][i] if i<rows-1 else 0
        # factorb = augmented_matrix[i-1][i] if i>0 else 0
        # if i>0:
        #     augmented_matrix[i-1,:] -=factorb*augmented_matrix[i,:]
        # if i<rows-1:
        #     augmented_matrix[i+1,:]-=factora*augmented_matrix[i,:]
        # Елементарні операції над рядками для отримання ступеневої форми
        for j in range(i+2):
            if j != i and j<rows:
                factor = augmented_matrix[j, i]
                augmented_matrix[j, :] -= factor * augmented_matrix[i, :]

    # Виокремлення оберненої матриці
    
    inverse_matrix = augmented_matrix[:, cols:]

    return inverse_matrix

if __name__=="__main__":
    try:
        for n in range(10,21):
            
            matrix, f = create_matrix(n)
            
            # Створення векторів з елементами трьох діагоналей(main_diagonal-для головної діагоналі,попередньо замінивши всі знаки в початковому векторі елементів діагоналі на протилежний)
            # а також a_diagonal-вектор елементів діагоналі що знаходиться під головною, b_diagonal-вектор елементів діагоналі що знаходиться над головною

            main_diagonal = [-matrix[i][i] for i in range(n)]
            a_diagonal = [0 if i==0 else matrix[i][i-1] for i in range(n)]
            b_diagonal = [0 if i==n-1 else matrix[i][i+1] for i in range(n)]
            


            #перевірка достатньої умови стійкості
            exisiting_of_i=False
            for i in range(n):
                if (x:=abs(main_diagonal[i]))>(y:=abs(a_diagonal[i])+abs(b_diagonal[i])):
                    exisiting_of_i=True
                elif x<y:
                    raise Exception(f"Не виконується перша умова стійкості в рядку №{i+1}")
            
            if not exisiting_of_i:
                raise Exception("Не виконується друга умова стійкості")
            

            #створення векторів для зберігання прогонкових коефіцієнтів
            alpha_list = list()
            beta_list = list()
            zet_list = list()

            #обрахунок прогонкових коефіцієнтів
            for i in range(n-1):
                if i == 0:
                    alpha_list.append(b_diagonal[0]/main_diagonal[0])
                    beta_list.append(f[0]/main_diagonal[0])
                else:
                    alpha_list.append(b_diagonal[i]/zet_list[i-1])
                    beta_list.append((f[i]+a_diagonal[i]*beta_list[i-1])/zet_list[i-1])
                zet_list.append(main_diagonal[i+1]-alpha_list[i]*a_diagonal[i+1])


            # Зворотній хід. Знаходження рішення СЛАР
            solution=list()
            for i in range(n):
                if i==0:
                    solution.append((f[n-i-1]+a_diagonal[n-i-1]*beta_list[n-i-2])/zet_list[n-i-2])
                else:
                    solution.append(alpha_list[n-i-1]*solution[i-1]+beta_list[n-i-1])
            
            # вектор відповідей треба відреверсити,адже в ньому x_n-1 = x0
                                                            #   x_n-2 = x1
                                                            #   ...
            solution.reverse()

            #Виведення рішення для поточної СЛАР(згідно поточного n)
            print(f"n={n}")
            for i,x in enumerate(solution):
                print(f"x{i}={x}")
            print()


            determ=-main_diagonal[0]
            for z in zet_list:
                determ*=-z
            print(f"Детермінант матриці={determ}")
            print()

            if determ!=0:
                matrix = numpy.array(matrix)
                inverse_matrix = inverse_matrix_gauss(matrix)
            
                
            
                matrix_columns:list[float]=[]
                sum=0
                for i in range(n):
                    sum=0
                    for j in range(n):
                        sum+=abs(matrix[i][j])
                    matrix_columns.append(sum)
                

                inverse_matrix_columns:list[float]=[]
                sum=0
                for i in range(n):
                    sum=0
                    for j in range(n):
                        sum+=abs(inverse_matrix[i][j])
                    inverse_matrix_columns.append(sum)
                
                matrix_norm = max(matrix_columns)
                inverse_matrix_norm = max(inverse_matrix_columns)

                print(f"Число обумовленості:{matrix_norm*inverse_matrix_norm}")

            
    except Exception as exc:
        print(exc)



