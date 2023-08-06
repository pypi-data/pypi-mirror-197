import pickle
from redis import Redis


# def func_add(a, b):
#     return (a + b)
#
#
# def dumps():
#     rds = Redis()
#     rds.set('demox', pickle.dumps(func_add))

def process_tax(result, callback_data):
    print(result)
    print(callback_data)
