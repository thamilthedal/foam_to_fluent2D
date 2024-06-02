import pandas as pd
import numpy as np

def read_data(file_name, start, stop):
    with open(file_name, 'r') as f:
        A = f.readlines()[start:stop]
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
    with open('./modules/console_log.txt', 'a') as f:
        if type(data) == list:
            for i in data:
                f.write(i)
        else:
            f.write(str(data))

def save_header(data, file_name):
    with open(f'./data/{file_name}.txt', 'w') as f:
        if type(data) == list:
            for i in data:
                f.write(i)
        else:
            f.write(data)

def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.readlines()


def get_file_info(file_list):
    for n, i in enumerate(file_list):
        if '(' in i:
            start_ID = n
            break

    for n, i in enumerate(file_list):
        if ')' in i:
            end_ID = n

    count = int(file_list[start_ID - 1].strip())
    return [count, file_list[start_ID:end_ID]]


def clean_and_split(row):
    return row.strip("(").strip(")\n").split()


def clean_and_split_face(row):
    return row.strip("(").strip(")\n").split("(")[1].split()

