# + tags=["parameters"]
upstream = ['process_data']
product = None
target_column = None
id_column = ''
list_column = None
# -

import os
import glob
import pandas as pd

os.makedirs(product['cleaned_csv'], exist_ok=True)

for file_path in glob.glob(os.path.join(upstream['process_data']['processed_data'], '*.csv')):
    df = pd.read_csv(file_path)

    target_cols = set(list_column or [])
    if target_column:
        target_cols.add(target_column)
    if id_column:
        target_cols.add(id_column)

    if target_cols:
        df_clean = df.dropna(subset=target_cols)
    else:
        df_clean = df.copy()

    output_filename = os.path.basename(file_path)
    df_clean.to_csv(os.path.join(product['cleaned_csv'], output_filename), index=False)
