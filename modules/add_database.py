import os
import pandas as pd

def add_database(i):
    if not os.path.isfile('./data/mesh_database.csv'):
        df = pd.DataFrame([i], columns = ["mesh_name", "ID", "dim", "R", "L", "Nr", "Nl", "BF", "Li", "Lo"])
        # print(df.head)
        df.to_csv('./data/mesh_database.csv', sep = '\t', index=None)
    else:
        df = pd.read_csv('./data/mesh_database.csv', sep = '\t')
        # print(df.head)
        df.loc[len(df)] = i
        df.to_csv('./data/mesh_database.csv', sep = '\t', index=None)
    
    print(f"{i[0]} Data Added")

