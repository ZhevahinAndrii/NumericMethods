import copy
import time
import math


import sympy
import numpy

import matplotlib.pyplot as plt
A = -5
B = 5


def func(x:float)-> float:
    return x**2 + 4*math.cos(x)

def newton_polynomial(x,results_in_nodes,max_polynomial_degree,nodes_set):
    
    x_set_for_table = copy.copy(nodes_set)
    y_set_for_table:list[float] = copy.copy(results_in_nodes)
    
    polynomial = 0
    polynomial +=y_set_for_table[0]
    
    for i in range(1,max_polynomial_degree+1):
        
        for j in range(len(y_set_for_table)-1):
            last_x = x_set_for_table[j+i] if j+i<=max_polynomial_degree else x_set_for_table[max_polynomial_degree]
            y_set_for_table[j] = (y_set_for_table[j+1]-y_set_for_table[j])/(last_x-x_set_for_table[j])
        
        
        multiplier = 1
        for index in range(i):
            multiplier *= (x - x_set_for_table[index])
        polynomial += y_set_for_table[0]*multiplier
        y_set_for_table.pop()
    return polynomial 


if __name__=="__main__":
    
        n:int = int(input("Input the amount of nodes:"))
        if(n<1):
            raise Exception("n must be bigger than 0")
        nodes_set = numpy.linspace(A,B,n,endpoint=True)
        max_polynomial_degree = n-1
        results_in_nodes = [func(x) for x in nodes_set]
        # print(f'Nodes:{nodes_set}')
        # print(f'Function result for nodes:{results_in_nodes}')
        
        x = sympy.symbols('x')
        polynom = newton_polynomial(x,results_in_nodes,max_polynomial_degree,nodes_set).factor().expand()
        
        print(polynom)
        x_set = [i/1000 for i in range(-5000,5001)]
        y_set_original = [func(x) for x in x_set]
        
        y_set_newton = [newton_polynomial(x,results_in_nodes,max_polynomial_degree,nodes_set) for x in x_set]
        
        interpolation_point = float(input('Input an interpolation point:'))
        start = time.time()
        y_in_interpolation = newton_polynomial(interpolation_point,results_in_nodes,max_polynomial_degree,nodes_set)
        end = time.time()
        print(f'Value in interpolation point:{y_in_interpolation}')
        print(f"Duration of Newton:{end-start:.10f}")
        plt.plot(x_set, y_set_original, label='Original Y', color='blue')
        plt.plot(x_set, y_set_newton, label='Newton Polynomial', color='g', linestyle='dashed')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.xlim([-5,5])
        plt.show()
        



    
