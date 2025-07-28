# + tags=["parameters"]
upstream = ['insert_ids']
product = None
list_column = None
# -

import os
import glob
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr, linregress

os.makedirs(product['generated_scatterplot'], exist_ok=True)

def analyze_correlation(x, y):
    mask = (~x.isna()) & (~y.isna())
    x = x[mask].astype(float)
    y = y[mask].astype(float)

    if len(x) < 3:
        return None

    r, p = pearsonr(x, y)
    slope, intercept, r_val, _, _ = linregress(x, y)
    residuals = y - (slope * x + intercept)
    outliers = (residuals.abs() > 2 * residuals.std()).sum()

    return {
        "pearson_r": r,
        "p_value": p,
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_val ** 2,
        "x_mean": x.mean(),
        "y_mean": y.mean(),
        "x_min": x.min(),
        "x_max": x.max(),
        "y_min": y.min(),
        "y_max": y.max(),
        "outlier_count": outliers
    }

def plot_correlation(df: pd.DataFrame, base_var: str, other_var: str, file_name: str) -> None:
    if base_var not in df.columns or other_var not in df.columns:
        return

    x = df[base_var]
    y = df[other_var]

    stats = analyze_correlation(x, y)

    if stats is None:
        return

    df['hover_text'] = df['ID']

    fig = px.scatter(
        df,
        x=base_var,
        y=other_var,
        hover_name='hover_text',
        trendline="ols",
        title=(f'Scatter Plot: {base_var} vs {other_var} - {file_name}'),
        labels={base_var: base_var, other_var: other_var}
    )

    fig.update_traces(marker=dict(size=6, opacity=0.7))

    out_html = os.path.join(product['generated_scatterplot'], f"{file_name}_{base_var}_vs_{other_var}.html")
    fig.write_html(out_html, include_plotlyjs='cdn')

    stats_csv = os.path.join(product['generated_scatterplot'], f"scatter_stats_{file_name}_{base_var}_vs_{other_var}.csv")
    stats_df = pd.DataFrame([{**{'x_column': base_var, 'y_column': other_var}, **stats}])
    stats_df.to_csv(stats_csv, index=False)

for file_path in glob.glob(os.path.join(upstream['insert_ids']['inserted_ids'], '*.csv')):
    df = pd.read_csv(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    if not list_column or len(list_column) < 2:
        continue

    for i in range(len(list_column)):
        for j in range(len(list_column)):
            if i != j:
                plot_correlation(df, list_column[i], list_column[j], file_name)
