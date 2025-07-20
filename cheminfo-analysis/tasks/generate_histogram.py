# + tags=["parameters"]
upstream = ['insert_ids']
product = None
target_column = None

# -

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

def compute_outliers_iqr(series: pd.Series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outlier_mask = (series < lower) | (series > upper)
    return outlier_mask.sum(), lower, upper

output_folder = product['generated_histograms']
os.makedirs(output_folder, exist_ok=True)

for csv_path in glob.glob(os.path.join(upstream['insert_ids']['inserted_ids'], '*.csv')):
    df = pd.read_csv(csv_path)
    filename = os.path.splitext(os.path.basename(csv_path))[0]

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

    out_path_img = os.path.join(output_folder, f'histogram_{filename}_{target_column}.png')
    plt.savefig(out_path_img, bbox_inches='tight')
    plt.clf()

    stats = values.describe()
    stats_dict = {
        'count': int(stats['count']),
        'mean': stats['mean'],
        'std': stats['std'],
        'min': stats['min'],
        '25%': stats['25%'],
        '50% (median)': stats['50%'],
        '75%': stats['75%'],
        'max': stats['max'],
        'skewness': skew(values),
        'kurtosis': kurtosis(values),
    }

    outlier_count, lower_bound, upper_bound = compute_outliers_iqr(values)
    stats_dict['outliers (IQR)'] = outlier_count
    stats_dict['IQR lower bound'] = lower_bound
    stats_dict['IQR upper bound'] = upper_bound

    out_path_csv = os.path.join(output_folder, f'histogram_stats_{filename}_{target_column}.csv')
    pd.DataFrame([stats_dict]).to_csv(out_path_csv, index=False)
