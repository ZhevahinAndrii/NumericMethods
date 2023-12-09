from exceptiongroup import catch
import numpy as np
from regex import F
import sympy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def first_equation(x:float,y:float,z:float):
    return x**2-y**2/9+z**2


def second_equation(x:float,y:float,z:float):
    return x**2/4+y**2+z**2/9-1



def jacobi_matrix(x_vector:list,z:float):
    size = len(x_vector)
    x,y = sympy.symbols("x y")
    equations = [first_equation(x,y,z),second_equation(x,y,z)]
    symbols = [x,y]
    
    A = np.identity(size)

    for i in range(size):
        for j in range(size):
            A[i][j] = sympy.diff(equations[i],symbols[j]).subs({x:x_vector[0],y:x_vector[1]})
    
    return A
def evaluate_L(x_vector:list,z:float):
    size = len(x_vector)
    x,y = sympy.symbols("x y")
    equations = [first_equation(x,y,z),second_equation(x,y,z)]
    symbols = [x,y]
    second_derivatives_result=[]

    for i in range(size):
        for j in range(size):
            try:
                second_derivatives_result.append(abs(sympy.diff(sympy.diff(equations[i],symbols[j]),symbols[j].subs({x:x_vector[0],y:x_vector[1]}))))
            except ValueError:
                second_derivatives_result.append(abs(sympy.diff(sympy.diff(equations[i],symbols[j]),symbols[j])))
    return max(second_derivatives_result)
def check_matrix_for_degeneration(x_vector:list,z:float):
    matrix = jacobi_matrix(x_vector,z)
    if np.linalg.det(matrix)==0:
        raise Exception("Matrix is degenerative(determinant=0)")
def evaluate_M(x_vector:list,z:float):
    matrix = jacobi_matrix(x_vector,z)
    inverted_matrix = np.linalg.inv(matrix)
    n = len(inverted_matrix)
    rows=[]
    for i in range(n):
        rows.append(sum(abs(elem) for elem in inverted_matrix[i]))

    inverted_matrix_norm = max(rows)
    return inverted_matrix_norm
def evaluate_beta(x:float,y:float,z:float):
    beta=max(abs(first_equation(x,y,z)),abs(second_equation(x,y,z)))
    return beta


def solve_newton(initial_approximation:tuple,epsilon:float):
    z_s = np.linspace(-5,-1,30)
    x_values = []
    y_values = []
    z_values = []

    start = time.time()
    
    
    for z in z_s:
        x,y = initial_approximation
        iteration_number=0
        max_iterations=100
        h = evaluate_M([x,y],z)**2*evaluate_L([x,y],z)*evaluate_beta(x,y,z)*4
        while iteration_number<=max_iterations:
            iteration_number+=1
            A = jacobi_matrix([x,y],z)
            F=np.array([first_equation(x,y,z),second_equation(x,y,z)])
            Z = np.linalg.solve(A,F)
            x,y = tuple(np.array([x,y])-Z)
            norm_z = np.linalg.norm(Z)
            # norm_z = max((abs(elem)for elem in Z))
        
            if norm_z<epsilon:
                x_values.append(x)
                y_values.append(y)
                z_values.append(z)
                break
        if iteration_number>max_iterations:
            print(f"Is not convergent for z={z} ")
        print(h)
    
    end=time.time()
    print(f"Execution time is {(end-start)*1000} milliseconds")
    return x_values,y_values,z_values

if __name__=="__main__":
    try:
        EPSILON = 1e-6
        initial_approximation = (.5,1.2)

        x_values,y_values,z_values = solve_newton(initial_approximation,EPSILON)

        for x,y,z in zip(x_values,y_values,z_values):
            print(f"Solution is {(x,y,z)}")
            print("Checking solution...")
            first_result="{:.2f}".format(first_equation(x,y,z))
            second_result="{:.2f}".format(second_equation(x,y,z))
            print(f"y1={first_result}\ny2={second_result}\n")

        print(f"Amount of values:{len(x_values)}")
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.plot(x_values, y_values, z_values, label='Intersection Curve', color='b', marker='o', linestyle='')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")


        plt.legend()
        plt.show()


       


    except Exception as e:
        print(e)





    