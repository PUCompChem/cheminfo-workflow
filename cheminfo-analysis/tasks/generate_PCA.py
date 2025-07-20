# + tags=["parameters"]
upstream = ['insert_ids']
product = None
list_column = None

# -

import os
import glob
import pandas as pd
import plotly.express as px
import plotly.io as pio
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def generate_2d_pca(data_standardized, ids, filename, features_used):
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(data_standardized)

    pca_df = pd.DataFrame({
        "PC1": principal_components[:, 0],
        "PC2": principal_components[:, 1],
        "ID": ids
    })

    grouped = pca_df.groupby(['PC1', 'PC2'])['ID'].apply(lambda x: '<br>'.join(sorted(x))).reset_index()
    grouped.rename(columns={'ID': 'All_IDs'}, inplace=True)

    fig = px.scatter(
        grouped,
        x="PC1",
        y="PC2",
        hover_name="All_IDs",
        title=f"2D PCA - {filename}<br><sub>Features used: {', '.join(features_used)}</sub>",
        labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2"}
    )

    fig.update_traces(marker=dict(size=5, opacity=0.7), textposition="top center")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=50))
    pio.write_html(fig, file=os.path.join(output_folder, f'pca_2d_{filename}.html'), auto_open=False)

def generate_3d_pca(data_standardized, ids, filename, features_used):
    pca = PCA(n_components=3)
    principal_components = pca.fit_transform(data_standardized)

    pca_df = pd.DataFrame({
        "PC1": principal_components[:, 0],
        "PC2": principal_components[:, 1],
        "PC3": principal_components[:, 2],
        "ID": ids
    })

    grouped = pca_df.groupby(['PC1', 'PC2', 'PC3'])['ID'].apply(lambda x: '<br>'.join(sorted(x))).reset_index()
    grouped.rename(columns={'ID': 'All_IDs'}, inplace=True)

    fig = px.scatter_3d(
        grouped,
        x="PC1",
        y="PC2",
        z="PC3",
        hover_name="All_IDs",
        title=f"3D PCA - {filename}<br><sub>Features used: {', '.join(features_used)}</sub>",
        labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2", "PC3": "Principal Component 3"}
    )

    fig.update_traces(marker=dict(size=5, opacity=0.7), textposition="top center")
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=50))
    pio.write_html(fig, file=os.path.join(output_folder, f'pca_3d_{filename}.html'), auto_open=False)

output_folder = product['generated_PCA']
os.makedirs(output_folder, exist_ok=True)

for csv_path in glob.glob(os.path.join(upstream['insert_ids']['inserted_ids'], '*.csv')):
    df = pd.read_csv(csv_path)
    filename = os.path.splitext(os.path.basename(csv_path))[0]

    try:
        df_filtered = df[['ID'] + list_column].dropna()
    except KeyError as e:
        print(f"Missing expected column(s) in {filename}: {e}")
        continue

    if df_filtered.shape[0] < 3:
        continue

    features = df_filtered[list_column].values
    X_scaled = StandardScaler().fit_transform(features)

    generate_2d_pca(X_scaled, df_filtered['ID'].values, filename, list_column)
    generate_3d_pca(X_scaled, df_filtered['ID'].values, filename, list_column)
