import ctypes

#dll_path =  'C:/Users/M K/Nextcloud/Python/PythonCpp/MathLib.dll'
dll_path = 'C:/Users/M K/Nextcloud/Python/PythonCppZajecia/addDLL.dll'
math_library = ctypes.CDLL(dll_path)

# Definiuj typy argumentów i wyników dla funkcji
math_library.Dodawanie.argtypes = [ctypes.c_int, ctypes.c_int]
math_library.Dodawanie.restype = ctypes.c_int

x = math_library.Dodawanie(4,6)
print(x)
