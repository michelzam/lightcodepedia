import time
import functools
import threading

call_depth = threading.local()
call_depth.depth = 0


def OLD__trace_execution_time(func, debug=False):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(call_depth, 'depth'):
            call_depth.depth = 0
        indent = '    ' * call_depth.depth
        start_time = time.time()
        print(f"{indent}-->: {func.__name__}")
        call_depth.depth += 1
        try:
            result = func(*args, **kwargs)
        finally:
            call_depth.depth -= 1
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"{indent}<--: {func.__name__} in {execution_time:.4f} seconds")
        return result
    return wrapper


import functools
import time
import inspect


class CallDepth:
    depth = 0


call_depth = CallDepth()

def trace_execution_time(func, debug=False):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(call_depth, 'depth'):
            call_depth.depth = 0
        indent = '    ' * call_depth.depth
        start_time = time.time()

        # Get the class name if the function is a method
        class_name = None
        if len(args) > 0:
            if hasattr(args[0], '__class__'):
                class_name = args[0].__class__.__name__

        # Get the parameter names and values
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        # params = ', '.join(f"{name}={value!r}" for name, value in bound_args.arguments.items())
        def label(value):
            result = f'{type(value).__name__}'
            if isinstance(value, str):
                result += f' = "`{value}`"'
            return result
        params = ', '.join(f"{name}: {label(value)}" for name, value in bound_args.arguments.items())

        if class_name:
            print(f"{indent}-->: {class_name}.{func.__name__}({params})")
        else:
            print(f"{indent}-->: {func.__name__}({params})")

        call_depth.depth += 1
        try:
            result = func(*args, **kwargs)
        finally:
            call_depth.depth -= 1
            end_time = time.time()
            execution_time = end_time - start_time
            if class_name:
                print(f"{indent}<--: {class_name}.{func.__name__} in {execution_time:.4f} seconds")
            else:
                print(f"{indent}<--: {func.__name__} in {execution_time:.4f} seconds")

        return result

    return wrapper


# # Example usage
# class Example:
#     @trace_execution_time
#     def method(self, x, y):
#         time.sleep(0.5)
#         return x + y
#
#
# @trace_execution_time
# def example_function(a, b, c=10):
#     time.sleep(0.5)
#     return a + b + c
#
#
# example = Example()
# example.method(1, 2)
#
# example_function(3, 4, c=5)

def print_stack():
    stack = inspect.stack()
    for frame in stack:
        print(f"Function '{frame.function}' in {frame.filename} at line {frame.lineno}")


def OLD_trace_execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"> '{func.__name__}' executed in {execution_time:.4f} seconds")
        return result
    return wrapper