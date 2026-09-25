print("THE FIRT ASSIGNMENT")
import numpy as np

l1=[1,2,3,4]
l2=[5,6,7,8]
l3=[9,10,11,12]
print("craeting array")
arr_1d=np.array([100,200,300,400,500,600])
arr_2d=np.array([l1,l2,l3])
print("1d array:",arr_1d)
print("2d array:",arr_2d)
print("\n")

print("2:indexing")
first_element=arr_1d[0]
last_element=arr_1d[-1]
element_2d=arr_2d[1,2]
print(f"First element of 1D:{first_element}")
print(f"last element of 1D:{last_element}")
print(f"element at row 1,column 2 in 2d:{element_2d}")
print()

print("3.slicing")
slice_1d=arr_1d[1:4]
sub_grid=arr_2d[0:2,1:3]
print("1d slice [1:4]:",slice_1d)
print("2d Sub-grid(Rows 0-1,cols 1-2):\n",sub_grid)
print()

print("4.vectorized operations")
a=np.array([1,2,3])
b=np.array([10,20,30])
addition=a+b
multiplication=a*10
squared=a**2
cube=a**3
sine_values=np.sin(a)
print("Vectorized Addition (a+b):",addition)
print("scalar multiplication (a*b):",multiplication)
print("vectorized cube()")
print("Element-wise Power (a**2)",squared)
print("sine values of 'a':",sine_values)
print()

print("5.BOOLEAN INDEXING (FILTERING)")
prices=np.array([15,80,45,120,30,95])
expensive_prices=prices[prices>50]
print(prices )
print(expensive_prices)