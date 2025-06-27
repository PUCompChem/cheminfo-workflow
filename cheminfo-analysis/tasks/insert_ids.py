# + tags=["parameters"]
upstream = ['clean_missing_values']
product = None

# -

import os
import glob
import pandas as pd

os.makedirs(product['inserted_ids'], exist_ok=True)

for file_path in glob.glob(os.path.join(upstream['clean_missing_values']['cleaned_csv'], '*.csv')):
    df = pd.read_csv(file_path)
    df.insert(0, 'ID', [f"ID_{i+1}" for i in range(len(df))])
    output_filename = os.path.basename(file_path)
    df.to_csv(os.path.join(product['inserted_ids'], output_filename), index=False)
