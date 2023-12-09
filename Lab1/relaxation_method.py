from math import sin,cos,log
import matplotlib.pyplot as plt
import numpy as np




EPSILON=1*10**(-4)
a:float = 2
b:float = 2.5

#definition of given function
def function(x:float):
    return x**2*cos(2*x)-1

#definition of derivative
def derivative(x:float):
    return 2*x*cos(2*x)-2*x**2*sin(2*x)

#checking the interval for having a root
def check_interval():
    if not function(a)*function(b)<0:
        raise Exception("Root of equation is not in the given interval [a;b]")


#checking interval for a sufficient condition for convergence
def check_interval_for_m1_and_M1():
    # on chosen interval we have growing function, so  minimum of its absolute value(m1) will be at the start of interval, maximum (M1) at the end
    m1 = abs(derivative(a))
    M1=abs(derivative(b))
    if m1<=0 or M1<=m1:
        raise Exception("The conditions of convergence are not met")
    return m1,M1

#derivative of function in chosen interval is>0,  so we choose "-" in formula

# xn+1 = xn - τf(xn).

if __name__=="__main__":
    try:
        x = np.linspace(0, 10, 100)
        y1 = x**2*np.cos(2*x)-1
        y2 = 2*x*np.cos(2*x)-2*x**2*np.sin(2*x)

        fig, axs = plt.subplots(2, 1, figsize=(7, 8))
        axs[0].plot(x, y1)
        axs[0].set_title('Графік функції')
        axs[0].grid(True,which='both')

        
        axs[1].plot(x, y2)
        axs[1].set_title('Графік похідної')
        axs[1].grid(True,which='both')

        plt.tight_layout()  
        plt.grid(True,which='both',axis='both')
        plt.show()

        
        check_interval()


        m1, M1 = check_interval_for_m1_and_M1()
        print(f"m1={m1},M1={M1}")


        #finding the optimal parameter
        topt=2/(m1+M1)
        print(f"Topt={topt}")


        

        #inputing the approximation
        approximation:float=float(input(f"Choose an approximation from given interval:[{a};{b}]: "))

        q0:float=(M1-m1)/(M1+m1)
        #      finding the maximum of |x0-x*| 
        temp=max(abs(approximation-a),abs(approximation-b))


        #evaluation of a priori estimate of iterations' number
        iterations=int((log(temp/EPSILON))/(log(1/q0)))+1
        print(f"A priori estimate of iterations' number:{iterations}")
        
        i=1
        while True:
            
            next_approximation=approximation-topt*function(approximation)
            print(f"Iteration {i}\t x{i}={next_approximation}")
            if abs(next_approximation-approximation)<=EPSILON:
                break
            else:
                approximation=next_approximation
                i+=1
        
    except Exception as exc:
        print(exc)
