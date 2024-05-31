import sys

def read_file(file_name):
    with open(file_name, 'r') as f:
        A = f.readlines()
    return A


def replace_options(file_list, R, L, Nr, Nl, BF, E1, E2):
    for n, i in enumerate(file_list):
        if '{r}' in i:
            file_list[n] =  i.replace('{r}', R)
        if '{l}' in i:
            file_list[n] =  i.replace('{l}', L)
        if '{a}' in i:
            file_list[n] =  i.replace('{a}', Nr)
        if '{b}' in i:
            file_list[n] =  i.replace('{b}', Nl)
        if '{bf}' in i:
            file_list[n] =  i.replace('{bf}', BF)
        if '{e1}' in i:
            file_list[n] =  i.replace('{e1}', E1)
        if '{e2}' in i:
            file_list[n] =  i.replace('{e2}', E2)
    return file_list

def write_file(file_list, file_name):
    with open(file_name, 'w') as f:
        for i in file_list:
             f.write(i)

def make_copy(arg_list):
    [R, L, Nr, Nl, BF, E1, E2] = arg_list
    sample_file = './sample/sample_blockMeshDict'
    sample = read_file(sample_file)
    file_contents = replace_options(sample,
                        R,
                        L,
                        Nr,
                        Nl,
                        BF,
                        E1,
                        E2)
    write_file(file_contents, 'test')

