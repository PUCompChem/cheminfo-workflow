# + tags=["parameters"]
upstream = ['clean_missing_values']
product = None
dist_matrix_type = None
clusters = None
method = None
name = None
value = None

# -

import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.cluster import KMeans

def find_threshold_for_n_clusters(Z, num_clusters) -> np.float64:
    distances = Z[:, 2]
    max_distance = distances.max()

    for threshold in np.linspace(0, max_distance, 1000):
        clusters = fcluster(Z, t=threshold, criterion='distance')
        if len(np.unique(clusters)) == num_clusters:
            return threshold

    return max_distance

def clusters_by_elbow(features) -> int:
    cluster_range = range(2, min(len(features), 21))
    inertia_values = []

    for n_clusters in cluster_range:
        if len(features) < n_clusters:
            break
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(features)
        inertia_values.append(kmeans.inertia_)

    if len(inertia_values) < 2:
        return 2

    first_derivative = np.diff(inertia_values)
    second_derivative = np.diff(first_derivative)
    elbow_index = np.argmin(second_derivative)
    optimal_clusters = cluster_range[elbow_index]

    return optimal_clusters

def clusters_by_silhouette(features) -> int:
    silhouette_scores = []
    cluster_range = range(2, min(len(features), 21))

    for n_clusters in cluster_range:
        if len(features) < n_clusters:
            break
        agglomerative = AgglomerativeClustering(n_clusters=n_clusters)
        cluster_labels = agglomerative.fit_predict(features)
        silhouette_avg = silhouette_score(features, cluster_labels)
        silhouette_scores.append(silhouette_avg)

    if not silhouette_scores:
        return 2

    max_index = np.argmax(silhouette_scores)
    optimal_clusters = cluster_range[max_index]

    return optimal_clusters

input_folder = upstream['clean_missing_values']['cleaned_csv']
csv_files = glob.glob(os.path.join(input_folder, '*.csv'))

os.makedirs(product['generated_clusters'], exist_ok=True)

for csv_path in csv_files:
    df = pd.read_csv(csv_path)

    if name not in df.columns or value not in df.columns:
        raise KeyError(f"Missing required columns in {csv_path}")

    features = df[[value]].dropna()
    raw_labels = df.loc[features.index, name].astype(str)
    short_labels = [f"ID_{i+1}" for i in range(len(raw_labels))]
    labels = short_labels

    label_map_df = pd.DataFrame({"ID": short_labels, "Original_Name": raw_labels})
    label_map_df.to_csv(os.path.join(product['generated_clusters'], f'label_mapping_{os.path.splitext(os.path.basename(csv_path))[0]}.csv'), index=False)

    distance_matrix = pdist(features.values, metric=dist_matrix_type)
    linked = linkage(distance_matrix, method=method)

    if clusters == 'elbow':
        num_clusters = clusters_by_elbow(features)
    elif clusters == 'silhouette':
        num_clusters = clusters_by_silhouette(features)
    elif isinstance(clusters, int) and 2 <= clusters <= min(len(features), 20):
        num_clusters = clusters
    else:
        raise ValueError("Invalid value for 'clusters'. Must be 'elbow', 'silhouette', or an integer between 2 and min(n_samples, 20).")

    cluster_labels = fcluster(linked, num_clusters, criterion='maxclust')

    silhouette_avg = silhouette_score(features, cluster_labels, metric=dist_matrix_type)
    davies_bouldin_avg = davies_bouldin_score(features, cluster_labels)
    calinski_harabasz_avg = calinski_harabasz_score(features, cluster_labels)

    threshold = find_threshold_for_n_clusters(linked, num_clusters)

    fig, ax = plt.subplots(figsize=(16, 9))
    dendrogram(
        linked,
        labels=labels,
        color_threshold=threshold - 0.1,
        above_threshold_color='black',
        orientation='top',
        show_contracted=True,
        leaf_font_size=6
    )

    ax.set_title('Hierarchical Clustering Dendrogram')
    ax.set_xlabel('IDs')
    ax.set_ylabel('Distance')
    ax.tick_params(axis='y', rotation=0, labelsize=8)
    plt.tight_layout()

    textstr = '\n'.join((
        f'Silhouette Score: {silhouette_avg:.4f}',
        f'Davies-Bouldin Score: {davies_bouldin_avg:.4f}',
        f'Calinski-Harabasz Score: {calinski_harabasz_avg:.4f}'
    ))

    ax.text(
        0.98, 0.96, textstr, transform=ax.transAxes,
        fontsize=12, verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.5)
    )

    filename = os.path.splitext(os.path.basename(csv_path))[0]

    fig.savefig(os.path.join(product['generated_clusters'], f'cluster_dendrogram_{filename}.png'), bbox_inches='tight')
    plt.close(fig)
