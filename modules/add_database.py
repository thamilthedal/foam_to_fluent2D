import os
import pandas as pd

def add_database(i):
    if not os.path.isfile('./data/mesh_database.csv'):
        df = pd.DataFrame([i], columns = ["mesh_name", "ID", "dim", "R", "L", "Nr", "Nl"])
        # print(df.head)
        df.to_csv('./data/mesh_database.csv', sep = '\t', index=None)
    else:
        df = pd.read_csv('./data/mesh_database.csv', sep = '\t')
        # print(df.head)
        df.loc[len(df)] = i
        df.to_csv('./data/mesh_database.csv', sep = '\t', index=None)
    
    print(f"{i[0]} Data Added")

# R = "4e-3"
# L = "1.5"

# mesh_settings = [
#         [R, L, "375", "100"],
#         [R, L, "750", "100"],
#         [R, L, "1500", "100"],
#         [R, L, "750", "120"],
#         [R, L, "750", "140"]
#         ]
# ID = "S320"

# for n, i in enumerate(mesh_settings):
#     data = [
#             f"M{n+1}-{ID}",
#             ID,
#             "2D",
#             i[0],
#             i[1],
#             i[3],
#             i[2]
#             ]
#     add_database(data)

