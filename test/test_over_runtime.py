# import functools
# from typing import Any

# def warr(pos):
#     class Wrapper:
#         def __init__(self, func) -> None:
#             self.func = func
#             functools.update_wrapper(self, func)
        
#         def __call__(self, *args, **kwargs) -> Any:
#             print(pos)
#             return self.func(*args, **kwargs)
        
#         def __get__(self, instance, owner):
#             if instance is None:
#                 return self
#             # This is the key part: creating a bound method
#             return functools.partial(self.__call__, instance)
            
#     return Wrapper

# class test1:
#     def __init__(self) -> None:
#         pass
    
#     @warr("hello")
#     def run(self):
#         print('hello1')

# a = test1()
# a.run()

def add_metadata(author, version):
    def decorator(func):
        func.author = author
        func.version = version
        return func
    return decorator

class MyClass:
    @add_metadata(author="John Doe", version="1.0")
    def my_method(self):
        print("Executing instance method...")

obj = MyClass()
print(obj.my_method.author)  # Output: John Doe
print(obj.my_method.version)  # Output: 1.0
obj.my_method()  # Output: Executing instance method...
