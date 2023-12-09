import time
import math
import copy

import sympy
import numpy

import matplotlib.pyplot as plt
A = -5
B = 5


def func(x:float)-> float:
    return x**2 + 4 * math.cos(x)

def polynomial_lagrange(x,n,nodes_set,results_in_nodes)->float:
    # if n==1:
    #     return 0
    polynomial = 0
    for i in range(n):
        numerator = 1
        denominator = 1
        for j in range(n):
            if j!=i:
                numerator*= (x-nodes_set[j])
                denominator *= (nodes_set[i]-nodes_set[j])
        polynomial += (numerator/denominator) * results_in_nodes[i]
    return polynomial

if __name__=="__main__":
    try:
        n:int = int(input("Input the amount of nodes:"))
        if(n<1):
            raise Exception("n must be bigger than 0")
        nodes_set = numpy.linspace(A,B,n,endpoint=True)

        max_polynomial_degree = n-1
        x = sympy.symbols('x')
        results_in_nodes = [func(x) for x in nodes_set]
        # print(f'Nodes:{nodes_set}')
        # print(f'Function result for nodes:{results_in_nodes}')
        polynomial = polynomial_lagrange(x,n,nodes_set,results_in_nodes).factor().expand()
        print(f'Polynomial:{polynomial}') 
        polynomial = sympy.Eq(polynomial,rhs=0)
        interpolation_point = float(input('Input an interpolation point:'))       
        start = time.time() 
        coefficients = polynomial.lhs.as_coefficients_dict()
        x_set_for_interpolation = [interpolation_point**i for i in range(n)]
    
        y_in_interpolation = 0
        for i in range(n):
            y_in_interpolation +=coefficients[x**i]*x_set_for_interpolation[i]
        end = time.time()

        print(f'Value in interpolation point:{y_in_interpolation}')
        print(f"Duration of Lagrange :{end-start:.10f}")
    

            
        x_set = [i/1000 for i in range(-5000,5001)]
        y_set_original = [func(x) for x in x_set]
        
        y_set_lagrange = [polynomial_lagrange(x,n,nodes_set,results_in_nodes) for x in x_set]
        

        
        # start = time.time()
        # y_set_newton = [divided_diff_table(x,results_in_nodes,max_polynomial_degree,nodes_set) for x in x_set]
        # end = time.time()
        # print(f"Duration of newton:{end-start}")
        plt.plot(x_set, y_set_original, label='Original Y', color='blue')
        plt.plot(x_set, y_set_lagrange, label='lagrange Polynomial', color='g', linestyle='dashed')
        # plt.plot(x_set,y_set_newton,label='Newton Polynomial',color='', linestyle='dashed')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.xlim([-5,5])
        plt.show()

    except Exception as exc:
        print(exc)

