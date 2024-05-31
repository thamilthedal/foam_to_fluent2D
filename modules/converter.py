import datetime
import pandas as pd

import modules.helper as ch


def point_convert():

    points_df = pd.read_csv('./data/points_data.csv', sep='\t')
    points_df.columns = ['ID', 'X', 'Y', 'Z']
    remove_index = points_df[points_df['Z'] != 0.0].index
    points_df = points_df.drop(index = remove_index)
    points_df = points_df.reset_index(drop=True)
    points_df['new_ID'] = points_df.index
    points_df.pop('Z')
    points_df.to_csv('./data/points_data.csv', sep='\t')
    print(f"Points Converted {datetime.datetime.now()}")


def get_order(row):
    order = []
    for n, i in enumerate(row[0:4]):
        if i != 'T':
            order.append(n)
    if order != [0, 3]:
        order.reverse()
    if len(order) < 2:
        print(order)
    return order


def get_hex_value(x):
    return str(hex(x)).replace("0x", "")

# Optimized function using the lookup dictionary
def replace_aligned(x, lookup_dict):
    return lookup_dict.get(x-1, None)  # Returns None if x-1 is not found

def convert_face_data(file_name, point_df):
    try:
        df = pd.read_csv(file_name, sep='\t')
        df.columns = ["ID", "N", "A", "B", "C", "D", "X1", "X2"]
        df.drop(columns=['N', 'ID'], inplace=True)

        # Get point IDs
        point_ID = point_df['ID']+1

        # Replace non-point IDs with 'T'
        df[['A', 'B', 'C', 'D']] = df[['A', 'B', 'C', 'D']].where(df[['A', 'B', 'C', 'D']].isin(point_ID.values), 'T')

        # print(f"Replace with T: {datetime.datetime.now()}")

        # Determine order of points
        df['order'] = df[['A', 'B', 'C', 'D']].apply(get_order, axis=1)

        # Extract N1 and N2 based on order
        df['N1'] = df.apply(lambda row: row.iloc[row['order'][0]], axis=1)
        df['N2'] = df.apply(lambda row: row.iloc[row['order'][1]], axis=1)

        # print(f"Reorder: {datetime.datetime.now()}")
        
        lookup_dict = {int(row['ID']):int(row['new_ID']+1) for _, row in point_df.iterrows()}
        # print(f"Lookup Dict: {datetime.datetime.now()}")
        # Replace misaligned
        df[['N1', 'N2']] = df[['N1', 'N2']].apply(lambda x: x.map(lambda y: replace_aligned(y, lookup_dict)))        
        # print(f"Replace Misaligned: {datetime.datetime.now()}")
 
        # Convert to hexadecimal
        df[['N1', 'N2', 'X1', 'X2']] = df[['N1', 'N2', 'X1', 'X2']].apply(lambda x: x.map(get_hex_value))

        # print(f"Hex Conversion: {datetime.datetime.now()}")
        
        # Save to file
        df[['N1', 'N2', 'X1', 'X2']].to_csv(file_name, sep='\t',
                                            index=False)  # Add index=False to avoid saving row indices
    except Exception as e:
        print(f"An error occurred in convert_face_data: {e}")


def face_convert(point_df):
    print("Faces\n")
    convert_face_data('./data/face_data.csv', point_df)
    print("Faces Over")


def boundary_convert(n_boundaries: int, point_df):
    for i in range(n_boundaries):
        print(f"Boundary {i + 1}\n")
        convert_face_data(f'./data/boundary_data_{i + 1}.csv', point_df)


def header_replace(line, X, Y):
    print(line)
    a = line.split()
    a[-1] = a[-1].replace(X, Y)
    b = " ".join(a)
    print(b)
    return b


def header_edits(n_boundaries: int):
    # Main Header
    header = ch.read_data('./data/header.txt', 0, -1)
    header[0] = header[0].replace("Fluent", "2D Fluent")
    header[3] = header[3].replace("3", "2")
    n_points = pd.read_csv('./data/points_data.csv', sep='\t').shape[0]
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
        boundary_header = ch.read_data(f'./data/boundary_header_{i + 1}.txt', 0, 1)
        boundary_header[0] = header_replace(boundary_header[0], "0", "2")
        ch.save_header(boundary_header, f'boundary_header_{i + 1}')
        count = boundary_header[0].split()[3]

    # Face Header
    face_header = ch.read_data('./data/face_header.txt', 0, 1)
    face_header[0] = header_replace(face_header[0], "0", "2")

    prev_count = header[8].split()[3]
    fh_intern = [header[8].replace(prev_count, count), '(0 "Interior Faces") \n \n', face_header[0]]
    face_header = fh_intern
    ch.save_header(face_header, 'face_header')

    # Node Header
    node_header = ch.read_data('./data/node_header.txt', 0, 1)
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
