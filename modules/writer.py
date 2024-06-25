import modules.helper as ch
import pandas as pd

def write_points(df, file_name, header_info):
    with open(file_name, "w") as f:
        header = header_info['header']
        # print(header)
        for i in header:
            f.write(i)
        f.write("\n")
        # print(type(df))
        for index, row in df.iterrows():
            f.write(f"\t{row['X']} {row['Y']}\n")
        f.write("))\n")

def write_3D_points(df, file_name, header_info):
    with open(file_name, "w") as f:
        header = header_info['header']
        # print(header)
        for i in header:
            f.write(i)
        f.write("\n")
        # print(type(df))
        for index, row in df.iterrows():
            f.write(f"\t{row['X']} {row['Y']} {row['Z']}\n")
        f.write("))\n")

def write_faces(face_df, boundary_df, file_name, n_boundaries, header_info):
    with open(file_name, 'a') as f:
        face_header = header_info['face_header']
        # print(face_header)
        for i in face_header:
            f.write(i)
        f.write("(\n")
        # print(type(df))
        for index, row in face_df.iterrows():
            f.write(f"\t{row['N1']} {row['N2']} {row['N']} {row['O']}\n")
        f.write("))\n")
        
        for n in range(n_boundaries):
            boundary_header = header_info['boundary_header'][n]
            # print(boundary_header)
            for i in boundary_header:
                f.write(i)
            f.write("(\n")
            # print(type(df))
            for index, row in boundary_df[n].iterrows():
                f.write(f"\t{row['N1']} {row['N2']} {row['N']} {row['O']}\n")
            f.write("))\n")

def write_others(file_name, header_info):
    with open(file_name, 'a') as f:
        node_header = header_info['node_header']
        # print(node_header)
        for i in node_header:
            f.write(i)
        f.write("\n")
        footer = header_info['footer']
        # print(footer)
        for i in footer:
            f.write(i)

def write_3D_faces(face_df, boundary_df, file_name, n_boundaries, header_info):
    with open(file_name, 'a') as f:
        face_header = header_info['face_header']
        # print(face_header)
        for i in face_header:
            f.write(i)
        f.write("(\n")
        # print(type(df))
        for index, row in face_df.iterrows():
            f.write(f"\t4 {row['A']} {row['B']} {row['C']} {row['D']} {row['N']} {row['O']}\n")
        f.write("))\n")
        
        for n in range(n_boundaries):
            boundary_header = header_info['boundary_header'][n]
            # print(boundary_header)
            for i in boundary_header:
                f.write(i)
            f.write("(\n")
            # print(type(df))
            for index, row in boundary_df[n].iterrows():
                f.write(f"\t4 {row['A']} {row['B']} {row['C']} {row['D']} {row['N']} {row['O']}\n")
            f.write("))\n")

