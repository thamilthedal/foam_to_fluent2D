import datetime
from modules.run import obtain_data, convert_data, write_data

def main():
    print(datetime.datetime.now())
    # obtain_data(sys.argv[1])
    obtain_data("./mesh_ground/fluentInterface/mesh_ground.msh", 5)
    print("Data Gathered\n")
    print(datetime.datetime.now())
    convert_data(5)
    print("Data Converted to 2D\n")
    print(datetime.datetime.now())
    write_data("./mesh_ground/fluentInterface/mesh_ground_converted.msh", 5)
    print("DONE\n")
    print(datetime.datetime.now())

if __name__ == "__main__":
    main()
