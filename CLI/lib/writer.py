def write_list(file, header_list):
    file.write("".join(header_list) + "\n")


def write_points(df, file_name, header_info):
    with open(file_name, "w") as f:
        write_list(f, header_info['header'])
        
        for index, row in df.iterrows():
            f.write(f"\t{row['X']} {row['Y']}\n")
        f.write("))\n")


def write_any_face(file, face_header, face_df):
    
    file.write("".join(face_header) + "(\n")

    for index, row in face_df.iterrows():
        file.write(f"\t{row['N1']:x} {row['N2']:x} {row['N']:x} {row['O']:x}\n")
    file.write("))\n")


def write_faces(face_df, boundary_df, file_name, n_boundaries, header_info):
    with open(file_name, 'a') as f:
        write_any_face(f, header_info['face_header'], face_df)
        
        for n in range(n_boundaries):
            write_any_face(f, header_info['boundary_header'][n], boundary_df[n])

def write_others(file_name, header_info):
    with open(file_name, 'a') as f:
        write_list(f, header_info['node_header'])
        write_list(f, header_info['footer'])
