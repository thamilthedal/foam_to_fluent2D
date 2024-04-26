import sys

def read_file(file_name):
    with open(file_name, 'r') as f:
        A = f.readlines()
    return A


def replace_options(file_list, R, L, A, B):
    for n, i in enumerate(file_list):
        if '{r}' in i:
            file_list[n] =  i.replace('{r}', R)
        if '{l}' in i:
            file_list[n] =  i.replace('{l}', L)
        if '{a}' in i:
            file_list[n] =  i.replace('{a}', A)
        if '{b}' in i:
            file_list[n] =  i.replace('{b}', B)
    
    return file_list

def write_file(file_list, file_name):
    with open(file_name, 'w') as f:
        for i in file_list:
             f.write(i)

def make_copy(arg_list):
    [R, L, A, B] = arg_list
    sample_file = './sample/sample_blockMeshDict'
    sample = read_file(sample_file)
    B = replace_options(sample,
                        R,
                        L,
                        A,
                        B)
    write_file(B, 'test')

