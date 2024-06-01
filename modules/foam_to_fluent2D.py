import datetime
from modules.run import obtain_data, convert_data, write_data

def main():
    
    start = datetime.datetime.now()
    print(start)
    n_boundaries = obtain_data()
    print("Data Gathered\n")
    print(datetime.datetime.now()-start)
    convert_data(n_boundaries)
    print("Data Converted to 2D\n")
    print(datetime.datetime.now()-start)
    write_data("./mesh_ground/fluentInterface/mesh_ground_converted.msh", n_boundaries)
    print("DONE\n")
    print(datetime.datetime.now()-start)

if __name__ == "__main__":
    main()
