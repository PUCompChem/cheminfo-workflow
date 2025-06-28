# + tags=["parameters"]
upstream = ['insert_ids']
product = None
target_column = None

# -

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs(product['generated_histograms'], exist_ok=True)

for csv_path in glob.glob(os.path.join(upstream['insert_ids']['inserted_ids'], '*.csv')):
    df = pd.read_csv(csv_path)

    if target_column not in df.columns:
        raise KeyError(f"Column '{target_column}' is required in {csv_path}")

    values = df[target_column].dropna().astype(float)

    plt.figure(figsize=(10, 6))
    plt.hist(values, bins=20, edgecolor='black')
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xlabel(f'{target_column} Value', fontweight='bold')
    plt.ylabel('Frequency', fontweight='bold')
    plt.title(f'Distribution of {target_column}', fontweight='bold')
    plt.tight_layout()

    filename = os.path.splitext(os.path.basename(csv_path))[0]
    out_path = os.path.join(product['generated_histograms'], f'histogram_{filename}_{target_column}.png')
    plt.savefig(out_path, bbox_inches='tight')
    plt.clf()