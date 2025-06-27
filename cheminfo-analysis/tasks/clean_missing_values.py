# + tags=["parameters"]
upstream = ['convert_xlsx_to_csv']
product = None

# -

import os
import glob
import pandas as pd

os.makedirs(product['cleaned_csv'], exist_ok=True)

for file_path in glob.glob(os.path.join(upstream['convert_xlsx_to_csv']['converted_xlsx_to_csv'], '*.csv')):
    df = pd.read_csv(file_path)

    df_clean = df.dropna()

    output_filename = os.path.basename(file_path)
    df_clean.to_csv(os.path.join(product['cleaned_csv'], output_filename), index=False)