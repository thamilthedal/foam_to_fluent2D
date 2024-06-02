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
    return lookup_dict.get(x, x)

def convert_face_data(df, points_df):
    # Get point IDs
    point_ID = points_df['ID']+1

    # Replace non-point IDs with 'T'
    df[['A', 'B', 'C', 'D']] = df[['A', 'B', 'C', 'D']].where(df[['A', 'B', 'C', 'D']].isin(point_ID.values), 'T')

    # Determine order of points
    df['order'] = df[['A', 'B', 'C', 'D']].apply(get_order, axis=1)

    # Extract N1 and N2 based on order
    df['N1'] = df.apply(lambda row: row.iloc[row['order'][0]], axis=1)
    df['N2'] = df.apply(lambda row: row.iloc[row['order'][1]], axis=1)
 
    # Create a Lookup Dictionary for speeding up the process
    lookup_dict = {int(row['ID']):int(row['new_ID'])+1 for _, row in points_df.iterrows()}

    # Replace misaligned
    df[['N1', 'N2']] = df[['N1', 'N2']].apply(lambda x: x.map(lambda y: replace_aligned(y, lookup_dict)))

    print(df.head)
    # df[['N1', 'N2']] = df[['N1', 'N2']].astype(int)
    print(df.head)

    # Convert to hexadecimal
    df[['N1', 'N2', 'N', 'O']] = df[['N1', 'N2', 'N', 'O']].apply(lambda x: x.map(get_hex_value))

    return df[['N1', 'N2', 'N', 'O']]


