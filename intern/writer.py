import helper as ch
import pandas as pd

def write_points(file_name):
    with open(file_name, "w") as f:
        header = ch.read_file('./header.txt')
        # print(header)
        for i in header:
            f.write(i)
        f.write("\n")
        df = pd.read_csv('./points_data.csv', sep = '\t')
        # print(df.head)
        # print(type(df))
        for index, row in df.iterrows():
            f.write(f"\t{row['X']} {row['Y']}\n")
        f.write("))\n")

def write_faces(file_name, n_boundaries):
    with open(file_name, 'a') as f:
        face_header = ch.read_file('./face_header.txt')
        # print(face_header)
        for i in face_header:
            f.write(i)
        f.write("(\n")
        df = pd.read_csv('./face_data.csv', sep = '\t')
        # print(df.head)
        # print(type(df))
        for index, row in df.iterrows():
            f.write(f"\t{row['N1']} {row['N2']} {row['X1']} {row['X2']}\n")
        f.write("))\n")
        
        for n in range(n_boundaries):
            boundary_header = ch.read_file(f'./boundary_header_{n+1}.txt')
            # print(boundary_header)
            for i in boundary_header:
                f.write(i)
            f.write("(\n")
            df = pd.read_csv(f'./boundary_data_{n+1}.csv', sep = '\t')
            # print(df.head)
            # print(type(df))
            for index, row in df.iterrows():
                f.write(f"\t{row['N1']} {row['N2']} {row['X1']} {row['X2']}\n")
            f.write("))\n")

def write_others(file_name):
    with open(file_name, 'a') as f:
        node_header = ch.read_file('./node_header.txt')
        # print(node_header)
        for i in node_header:
            f.write(i)
        f.write("\n")
        footer = ch.read_file('./footer.txt')
        # print(footer)
        for i in footer:
            f.write(i)

