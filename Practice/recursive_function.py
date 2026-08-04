def factorial(n):
    if n==1 or n==0:
        return 1
    else:
        fact= n*factorial(n-1)
        return fact
print(f"The Factorial of 5 is: {factorial(5)}")
print(f"The Factorial of 10 is: {factorial(3)}")

def fiboo(n):
    if n==0:
        return 0 
    elif n==1:
        return 1
    else:
        fibonacci=fiboo(n-1)+fiboo(n-2)
        return fibonacci

print(f"The Fibonacci of number 5 is: {fiboo(5)}")


cube=lambda n:n**3
print(f"the cube of {5} is: {cube(5)}")
l1=[1,2,3,4,5]
print("The list is: ",l1)
l2=list(map(lambda x:x**3,l1))
l3=list(filter(lambda x:x%2==0,l1))
print(f"The cube of list is: {l2}")
print(f"The even number of list is: {l3}")