# + tags=["parameters"]
upstream = ['process_data']
product = None

# -

import os
import glob
import pandas as pd

os.makedirs(product['cleaned_csv'], exist_ok=True)

for file_path in glob.glob(os.path.join(upstream['process_data']['processed_data'], '*.csv')):
    df = pd.read_csv(file_path)

    df_clean = df.dropna()

    output_filename = os.path.basename(file_path)
    df_clean.to_csv(os.path.join(product['cleaned_csv'], output_filename), index=False)