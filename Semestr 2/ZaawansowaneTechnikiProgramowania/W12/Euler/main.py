import ctypes
from timeit import default_timer as timer
import math

# Wczytaj bibliotekę DLL
#C:\Users\M K\Nextcloud\Python\PythonCsharp\MathDLL\MathDLL\bin\Release\netstandard2.0
#dll_path = 'C:/Users/M K/Nextcloud/Python/PythonCsharp/MathDLL.dll'
#dll_path = 'MathLib.dll'
dll_path =  'C:/Users/M K/Nextcloud/Python/PythonCpp/MathLib.dll'
math_library = ctypes.CDLL(dll_path)

#print(math_library.MultiplyDouble(5.0,4.5))

# Definiuj typy argumentów i wyników dla funkcji
math_library.MultiplyDouble.argtypes = [ctypes.c_double, ctypes.c_double]
math_library.MultiplyDouble.restype = ctypes.c_double

math_library.MultiplyInt.argtypes = [ctypes.c_int, ctypes.c_int]
math_library.MultiplyInt.restype = ctypes.c_int

math_library.SquareInt.argtypes = [ctypes.c_int]
math_library.SquareInt.restype = ctypes.c_int

math_library.Factorial.argtypes = [ctypes.c_int]
math_library.Factorial.restype = ctypes.c_int

math_library.Euler.argtypes = [ctypes.c_int]
math_library.Euler.restype = ctypes.c_double

# Użyj funkcji z DLL
result_float = math_library.MultiplyDouble(3.3, 4.0)
result_int = math_library.MultiplyInt(3, 4)
result_squareint = math_library.SquareInt(5)
result_factorial = math_library.Factorial(5)
result_euler = math_library.Euler(34)

print(f"Float multiplication result: {result_float}")
print(f"Integer multiplication result: {result_int}")
print(f"Power of two: {result_squareint}")
print(f"Factorial: {result_factorial}")
print(f"Euler: {result_euler}")

#porownanie czasów
#full dll
t0 = timer()
result1 = math_library.Euler(34)
t1 = timer()-t0
print(result1)
print(f'Czas dll:{t1}')

#python + factorial dll
t0 = timer()
result2 = 0
for i in range(34):
    result2 += 1/math_library.Factorial(i)
t1 = timer()-t0
print(result2)
print(f'Czas python + factorial dll:{t1}')

#python
t0 = timer()
result3 = 0
for i in range(34):
    result3 += 1/math.factorial(i)
t1 = timer()-t0
print(result3)
print(f'Czas python + math factorial:{t1}')

#python
def fact(n):
    if (n == 0 or n == 1):
        return 1

    result = 1
    for i in range(2, 34):
        result *= i
    
    return result

t0 = timer()
result4 = 0
for i in range(34):
    result4 += 1/fact(i)
t1 = timer()-t0
print(result4)
print(f'Czas python + python factorial:{t1}')