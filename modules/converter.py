import datetime
import pandas as pd

import modules.helper as ch


def point_convert(points_df):
    remove_index = points_df[points_df['Z'] != '0'].index
    points_df['ID'] = points_df.index
    points_df = points_df.drop(index = remove_index)
    points_df = points_df.reset_index(drop=True)
    points_df['new_ID'] = points_df.index
    points_df.pop('Z')
    print(f"Points Converted {datetime.datetime.now()}")
    return points_df


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

def replace_aligned(x, lookup_dict):
    return lookup_dict.get(x-1, None)  # Returns None if x-1 is not found

def convert_face_data(df, point_df):
    try:
        df.drop(columns=['X'], inplace=True)

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
        
        # Create a Lookup Dictionary for speeding up the process
        lookup_dict = {int(row['ID']):int(row['new_ID']+1) for _, row in point_df.iterrows()}
        # print(f"Lookup Dict: {datetime.datetime.now()}")

        # Replace misaligned
        df[['N1', 'N2']] = df[['N1', 'N2']].apply(lambda x: x.map(lambda y: replace_aligned(y, lookup_dict)))        
        # print(f"Replace Misaligned: {datetime.datetime.now()}")
 
        # Convert to hexadecimal
        df[['N1', 'N2', 'N', 'O']] = df[['N1', 'N2', 'N', 'O']].apply(lambda x: x.map(get_hex_value))

        # print(f"Hex Conversion: {datetime.datetime.now()}")
        
        # Remove other columns that are not needed for writing
        df.drop(columns=['A', 'B', 'C', 'D', 'order'], inplace=True)
        return df
    except Exception as e:
        print(f"An error occurred in convert_face_data: {e}")


def face_convert(face_df, point_df):
    print("Faces\n")
    face_df = convert_face_data(face_df, point_df)
    print("Converted!")


def boundary_convert(boundary_df, n_boundaries: int, point_df):
    final_boundary_data = []
    for i in range(n_boundaries):
        print(f"Boundary {i + 1}\t")
        final_boundary_data.append(convert_face_data(boundary_df[i], point_df))
        print(f"Converted!")
    return final_boundary_data

def header_replace(line, X, Y):
    a = line.split()
    a[-1] = a[-1].replace(X, Y)
    b = " ".join(a)
    return b


def header_edits(points_df, n_boundaries: int, header_info):
    # Main Header
    header = header_info['header']
    header[0] = header[0].replace("Fluent", "2D Fluent")
    header[2] = header[2].replace("3", "2")
    n_points = points_df.shape[0]
    y = get_hex_value(n_points)
    header[4] = header[4].replace(header[4].split()[3], y, 1)
    header[4] = header_replace(header[4], "3", "2")
    header[7] = header[7].replace(header[7].split()[3], y, 1)
    header[7] = header[7].replace("3)", "2)") 
    header.append("(")

    count = 0
    # Boundary Header
    for i in range(n_boundaries):
        boundary_header = header_info['boundary_header'][i]
        boundary_header[0] = header_replace(boundary_header[0], "0", "2")
        header_info['boundary_header'][i] = boundary_header
        count = boundary_header[0].split()[3]


    # Face Header
    face_header = header_info['face_header']
    face_header[0] = header_replace(face_header[0], "0", "2")
    prev_count = header[6].split()[3]
    fh_intern = [header[6].replace(prev_count, count), '(0 "Interior Faces") \n \n', face_header[0]]
    face_header = fh_intern
    header_info['face_header'] = face_header

    # Node Header
    node_header = header_info['node_header']
    NH = node_header[0][:-2] + ')'
    NH = header_replace(NH, "0", "3")
    node_header[0] = header[5]
    node_header.append(NH)
    header_info['node_header'] = node_header

    header = header[0:3] + [header[4]] + header[7:-1]
    header_info['header'] = header

    print(f"\nHeader Edits Done {datetime.datetime.now()}")

    return header_info
    # Footer - No EDITS
