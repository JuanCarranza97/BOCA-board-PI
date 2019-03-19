def function_1():
    print("Hola 1")

def function_2():
    print("Hola 2")

class function:
    def __init__(self,name,callBack):
        self.name     = name
        self.callBack = callBack

functions = []
functions.append(function("Uno",function_1))
functions.append(function("Dos",function_2))


functions[1].callBack()
