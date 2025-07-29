# + tags=["parameters"]
upstream = ['clean_missing_values']
product = None
id_column = None
# -

import os
import glob
import pandas as pd

os.makedirs(product['inserted_ids'], exist_ok=True)

for file_path in glob.glob(os.path.join(upstream['clean_missing_values']['cleaned_csv'], '*.csv')):
    df = pd.read_csv(file_path)
    output_filename = os.path.basename(file_path)

    if id_column and id_column in df.columns:
        df = df.rename(columns={id_column: 'ID'})
    else:
        df.insert(0, 'ID', [f"ID_{i+1}" for i in range(len(df))])

    df.to_csv(os.path.join(product['inserted_ids'], output_filename), index=False)
