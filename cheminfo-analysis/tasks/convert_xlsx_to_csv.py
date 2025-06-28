# + tags=["parameters"]
upstream = None
folder_input = None
product = None

# -

import pandas as pd
import os
import glob

os.makedirs(product['converted_xlsx_to_csv'], exist_ok=True)

for file_path in glob.glob(os.path.join(folder_input, '*.xlsx')):
    df = pd.read_excel(file_path, engine='openpyxl')
    output_filename = os.path.splitext(os.path.basename(file_path))[0] + ".csv"
    df.to_csv(os.path.join(product['converted_xlsx_to_csv'], output_filename), index=False)