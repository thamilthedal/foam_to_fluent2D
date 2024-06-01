import pandas as pd
import numpy as np

def read_data(file_name, start, stop):
    with open(file_name, 'r') as f:
        A = f.readlines()[start:stop]
    return A

def read_file(file_name):
    with open(file_name, 'r') as f:
        A = f.readlines()
    return A

def get_face_data(file_name, skip, n_rows):

    A = pd.DataFrame(np.genfromtxt(
        file_name,
        skip_header = skip,
        max_rows = n_rows,
        dtype = "int32",
        converters={_: lambda s: int(s, 16) for _ in range(7)},
        ))

    return A

def log_data(data):
    with open('./console_log.txt', 'a') as f:
        if type(data) == list:
            for i in data:
                f.write(i)
        else:
            f.write(str(data))

def save_header(data, file_name):
    with open(f'./{file_name}.txt', 'w') as f:
        if type(data) == list:
            for i in data:
                f.write(i)
        else:
            f.write(data)


