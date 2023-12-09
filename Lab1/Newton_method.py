from math import sin,cos,log,log2
import matplotlib.pyplot as plt
import numpy as np

EPSILON=1*10**(-4)
a:float = 2.3
b:float=2.5


#definition of the function
def function(x:float):
    return x**2*cos(2*x)-1

#definition of the functions' derivative
def derivative(x:float):
    return 2*x*cos(2*x)-2*x**2*sin(2*x)

#as we need it in this method, the definition of the second derivative
def second_derivative(x:float):
    return 2*(cos(2*x)-2*x*sin(2*x))-2*(2*x*sin(2*x)+2*x**2*cos(2*x))

#checking the interval for having a root
def check_interval():
    if not function(a)*function(b)<0:
        raise Exception("Root of equation is not in the given interval [a;b]")


# cause on interval [2.3;2.5] function's second derivative is going down
def check_interval_for_positive_second_derivative():
    if not (second_derivative(b)>0):
        raise Exception("Second derivative on this interval is < 0")


#cause we have growing derivative on interval [2.3;2.5], we need to check if derivative in a is > 0 or , if it <0, so we also need derivative in b be <0
def check_derivative_for_not_equal_to_null_on_interval():
    if not derivative(a)>0 or (derivative(a)<0 and derivative(b)<0):
        raise Exception("f'(x)=0 in this interval")


#checking the first sufficient condition for convergence
def check_approximation(x:float):
    if not function(x)*second_derivative(x)>0:
        raise Exception("You have chosen the wrong approximation")


def get_m1_and_M2():
    
    m1 = abs(derivative(a))
    M2=abs(second_derivative(a))

    return (m1,M2)


if __name__=="__main__":
    try:
        x = np.linspace(-5, 5,1000)
        y1 = x**2*np.cos(2*x)-1
        y2 = 2*x*np.cos(2*x)-2*x**2*np.sin(2*x)
        y3=2*(np.cos(2*x)-2*x*np.sin(2*x))-2*(2*x*np.sin(2*x)+2*x**2*np.cos(2*x))
        fig, axs = plt.subplots(3, 1, figsize=(7, 8))
        axs[0].plot(x, y1)
        axs[0].set_title('Графік функції')
        axs[0].grid(True,which='both')

        
        axs[1].plot(x, y2)
        axs[1].set_title('Графік похідної')
        axs[1].grid(True,which='both')
        
        
        axs[2].plot(x,y3)
        axs[2].set_title('Графік другої похідної')
        axs[2].grid(True,which='both')

        plt.tight_layout()  
        plt.grid(True,which='both',axis='both')
        plt.show()


        check_interval()
        check_interval_for_positive_second_derivative()
        check_derivative_for_not_equal_to_null_on_interval()

        approximation:float=float(input(f"Choose an approximation from given interval:[{a};{b}]: "))

        #checking the first sufficient condition for convergence
        check_approximation(approximation)

        #getting m1 and M2 values
        m1,M2=get_m1_and_M2()
        print(f"m1={m1},M2={M2}")

       # finding the maximum of |x0-x*| 
        temp=max(abs(approximation-a),abs(approximation-b))
        
        q:float = (M2*temp)/(2*m1)
        print(f"q={q}")
        #checking the second sufficient condition for convergence
        if not q<1:
            raise Exception("q>1")
        
        #evaluation of a priori estimate of iterations' number
        iterations=int(log2(log(temp/EPSILON)/log(1/q)+1))+1
        
        print(f"A priori estimate of iterations' number:{iterations}")
                
        i=1
        while True:
            next_approximation = approximation - function(approximation)/derivative(approximation)
            print(f"Iteration {i}\t x{i}={next_approximation}")
            if abs(next_approximation-approximation)<=EPSILON:
                break
            else:
                approximation=next_approximation
                i+=1
        
    except Exception as exc:
        print(exc)