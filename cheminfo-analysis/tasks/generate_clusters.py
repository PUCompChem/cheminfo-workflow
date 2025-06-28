# + tags=["parameters"]
upstream = ['insert_ids']
product = None
dist_matrix_type = None
clusters = None
clust_method = None
target_column = None

# -

import os
import glob
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.io as pio
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from sklearn.metrics import silhouette_score
from sklearn.cluster import AgglomerativeClustering, KMeans

def find_threshold_for_n_clusters(Z, num_clusters) -> float:
    distances = Z[:, 2]
    max_distance = distances.max()
    for threshold in np.linspace(0, max_distance, 1000):
        clusters = fcluster(Z, t=threshold, criterion='distance')
        if len(np.unique(clusters)) == num_clusters:
            return threshold
    return max_distance

def clusters_by_elbow(features) -> int:
    inertia_values = []
    cluster_range = range(2, min(len(features), 21))
    for n_clusters in cluster_range:
        if len(features) < n_clusters:
            break
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(features)
        inertia_values.append(kmeans.inertia_)
    if len(inertia_values) < 2:
        return 2
    second_derivative = np.diff(np.diff(inertia_values))
    elbow_index = np.argmin(second_derivative)
    return cluster_range[elbow_index]

def clusters_by_silhouette(features) -> int:
    silhouette_scores = []
    cluster_range = range(2, min(len(features), 21))
    for n_clusters in cluster_range:
        if len(features) < n_clusters:
            break
        model = AgglomerativeClustering(n_clusters=n_clusters).fit(features)
        score = silhouette_score(features, model.labels_)
        silhouette_scores.append(score)
    return cluster_range[np.argmax(silhouette_scores)] if silhouette_scores else 2

output_folder = product['generated_clusters']
os.makedirs(output_folder, exist_ok=True)

for csv_path in glob.glob(os.path.join(upstream['insert_ids']['inserted_ids'], '*.csv')):
    df = pd.read_csv(csv_path)
    filename = os.path.splitext(os.path.basename(csv_path))[0]

    df_filtered = df[['ID', target_column]].dropna()
    if df_filtered.shape[0] < 3:
        continue

    features = df_filtered[[target_column]].values
    labels = df_filtered['ID'].values

    dist_matrix = pdist(features, metric=dist_matrix_type)
    linked = linkage(dist_matrix, method=clust_method)

    if clusters == 'elbow':
        num_clusters = clusters_by_elbow(features)
    elif clusters == 'silhouette':
        num_clusters = clusters_by_silhouette(features)
    elif isinstance(clusters, int):
        num_clusters = clusters
    else:
        raise ValueError("Invalid 'clusters' value")

    threshold = find_threshold_for_n_clusters(linked, num_clusters)

    fig = ff.create_dendrogram(
        features,
        labels=labels,
        linkagefun=lambda x: linkage(x, method=clust_method),
        color_threshold=threshold - 0.1,
        orientation='bottom'
    )

    fig.update_layout(
        width=1500,
        height=700,
        title=f"Cluster Dendrogram - {filename}"
    )

    output_file = os.path.join(output_folder, f'dendrogram_{filename}.html')
    pio.write_html(fig, file=output_file, auto_open=False)
