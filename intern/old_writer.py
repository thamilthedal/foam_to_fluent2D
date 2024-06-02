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

def header_replace(line, X, Y):
    print(line)
    a = line.split()
    a[-1] = a[-1].replace(X, Y)
    b = " ".join(a)
    print(b)
    return b


def header_edits(n_boundaries: int):
    # Main Header
    header = ch.read_data('./header.txt', 0, -1)
    header[0] = header[0].replace("Fluent", "2D Fluent")
    header[3] = header[3].replace("3", "2")
    n_points = pd.read_csv('./points_data.csv', sep='\t').shape[0]
    y = get_hex_value(n_points)
    header[6] = header[6].replace(header[6].split()[3], y, 1)
    header[6] = header_replace(header[6], "3", "2")
    header[-1] = header[-1].replace(header[-1].split()[3], y, 1)
    header[-1] = header_replace(header[-1], "3", "2")
    header.append("(")
    # print(header)

    count = 0
    # Boundary Header
    for i in range(n_boundaries):
        boundary_header = ch.read_data(f'./boundary_header_{i + 1}.txt', 0, 1)
        boundary_header[0] = header_replace(boundary_header[0], "0", "2")
        ch.save_header(boundary_header, f'boundary_header_{i + 1}')
        count = boundary_header[0].split()[3]

    # Face Header
    face_header = ch.read_data('./face_header.txt', 0, 1)
    face_header[0] = header_replace(face_header[0], "0", "2")

    prev_count = header[8].split()[3]
    fh_intern = [header[8].replace(prev_count, count), '(0 "Interior Faces") \n \n', face_header[0]]
    face_header = fh_intern
    ch.save_header(face_header, 'face_header')

    # Node Header
    node_header = ch.read_data('./node_header.txt', 0, 1)
    NH = node_header[0][:-2] + ')'
    NH = header_replace(NH, "0", "3")
    node_header[0] = header[7]
    node_header.append(NH)
    # print(node_header)
    ch.save_header(node_header, 'node_header')

    header = header[0:4] + [header[6]] + header[10:]
    # print(header)
    ch.save_header(header, 'header')

    print(f"\nHeader Edits Done {datetime.datetime.now()}")

    # Footer - No EDITS
