import numpy as np
import os
from concurrent import futures


def func_transformer(func):
    '''
    transform this kind of function:
    ```
    def demo_func(x):
        x1, x2, x3 = x
        return x1 ** 2 + x2 ** 2 + x3 ** 2
    ```
    into this kind of function:
    ```
    def demo_func(x):
        x1, x2, x3 = x[:,0], x[:,1], x[:,2]
        return x1 ** 2 + (x2 - 0.05) ** 2 + x3 ** 2
    ```
    getting vectorial performance if possible
    :param func:
    :return:
    '''

    prefered_function_format = '''
    def demo_func(x):
        x1, x2, x3 = x[:, 0], x[:, 1], x[:, 2]
        return x1 ** 2 + (x2 - 0.05) ** 2 + x3 ** 2
    '''

    is_vector = getattr(func, 'is_vector', False)
    if is_vector:
        return func
    else:
        if func.__code__.co_argcount == 1:
            def func_transformed(X):
                output = []
                with futures.ProcessPoolExecutor() as pool:
                    for result in pool.map(func, X):
                        output.append(result)

                return np.array(output)

            return func_transformed
        elif func.__code__.co_argcount > 1:

            def func_transformed(X):
                return np.array([func(*tuple(x)) for x in X])

            return func_transformed

    raise ValueError('''
    object function error,
    function should be like this:
    ''' + prefered_function_format)
