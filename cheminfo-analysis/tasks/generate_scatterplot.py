# + tags=["parameters"]
upstream = ['insert_ids']
product = None
list_column = None

# -

import os
import glob
import pandas as pd
import plotly.express as px

os.makedirs(product['generated_scatterplot'], exist_ok=True)


def get_name(var) -> str:
    return var


def plot_correlation(df: pd.DataFrame, base_var: str, other_var: str, file_name: str) -> None:
    if base_var not in df.columns or other_var not in df.columns:
        return

    df = df.dropna(subset=[base_var, other_var])
    if df.empty:
        return

    df['x'] = df[base_var].round(5)
    df['y'] = df[other_var].round(5)

    grouped = df.groupby(['x', 'y'])['ID'].apply(lambda ids: '<br>'.join(sorted(ids))).reset_index()
    grouped.rename(columns={'x': base_var, 'y': other_var, 'ID': 'All_IDs'}, inplace=True)

    fig = px.scatter(
        grouped,
        x=base_var,
        y=other_var,
        hover_name='All_IDs',
        title=f'Scatter Plot: {base_var} vs {other_var} - {file_name}',
        labels={base_var: get_name(base_var), other_var: get_name(other_var)}
    )

    out_html = os.path.join(product['generated_scatterplot'], f"{file_name}_{base_var}_vs_{other_var}.html")
    fig.write_html(out_html, include_plotlyjs='cdn')


for file_path in glob.glob(os.path.join(upstream['insert_ids']['inserted_ids'], '*.csv')):
    df = pd.read_csv(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    if not list_column or len(list_column) < 2:
        continue

    for i in range(len(list_column)):
        for j in range(len(list_column)):
            if i != j:
                plot_correlation(df, list_column[i], list_column[j], file_name)
