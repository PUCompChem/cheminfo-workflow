# + tags=["parameters"]
upstream = ['insert_ids']
product = None
target_column = None
dist_matrix_type = None

# -

import pandas as pd
import numpy as np
import os
import glob
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics.pairwise import cosine_similarity

def calculate_distance_matrix(data_array: np.ndarray, dist_type: str) -> np.ndarray:
    if dist_type in ['euclidean', 'cityblock']:
        return squareform(pdist(data_array, metric=dist_type))
    elif dist_type == 'cosine':
        sim_matrix = cosine_similarity(data_array)
        dist_matrix = 1 - sim_matrix
        np.fill_diagonal(dist_matrix, 0)
        return dist_matrix
    else:
        raise ValueError(f"Unsupported distance type: {dist_type}")

os.makedirs(product['calculated_dist_matrix'], exist_ok=True)

for path in glob.glob(os.path.join(upstream['insert_ids']['inserted_ids'], '*.csv')):
    df = pd.read_csv(path)
    filename = os.path.splitext(os.path.basename(path))[0]

    if 'ID' not in df.columns or not target_column:
        continue

    names = df['ID'].astype(str).values
    values = df[[target_column]].values

    distance_matrix = calculate_distance_matrix(values, dist_matrix_type)

    dist_df = pd.DataFrame(distance_matrix, index=names, columns=names)
    output_path = os.path.join(product['calculated_dist_matrix'], f"dist_matrix_of_{filename}.csv")
    dist_df.to_csv(output_path, index=True)
