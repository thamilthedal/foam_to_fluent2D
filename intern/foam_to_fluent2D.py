import datetime
import converter as cc
import writer as cw
from reader import obtain_data
import pandas as pd

def convert_data(n_boundaries):
    cc.point_convert()
    point_df = pd.read_csv('./points_data.csv', sep='\t')
    point_df = point_df.astype({"ID": 'int', "new_ID": 'int'})
    cc.face_convert(point_df)
    cc.boundary_convert(n_boundaries, point_df)
    cc.header_edits(n_boundaries)


def write_data(output_file, n_boundaries):
    cw.write_points(output_file)
    cw.write_faces(output_file, n_boundaries)
    cw.write_others(output_file)



def main():
    start = datetime.datetime.now()
    print(start)
    n_boundaries = obtain_data()
    print("Data Gathered\n")
    print(datetime.datetime.now()-start)
    convert_data(n_boundaries)
    print("Data Converted to 2D\n")
    print(datetime.datetime.now()-start)
    write_data("./mesh_ground_converted.msh", n_boundaries)
    print("DONE\n")
    print(datetime.datetime.now()-start)

if __name__ == "__main__":
    main()
