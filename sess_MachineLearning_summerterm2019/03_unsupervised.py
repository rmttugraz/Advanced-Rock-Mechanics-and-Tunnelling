# -*- coding: utf-8 -*-

# This code loads the data that was generated by '00_data_generator.py' and
# and then applies a simple machine learning pipeline to create a machine
# learning model that learns how to separate gneiss from marl according to the
# features tensile strength and unconfined compressive strength

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import MeanShift, KMeans, AgglomerativeClustering
from sklearn.metrics import accuracy_score


###############################################################################
# load data

df_gneiss = pd.read_csv('gneiss.csv')
df_marl = pd.read_csv('marl.csv')

###############################################################################
# preprocessing is done to create a dataset that is suitable for supervised
# learning: one big dataframe with all samples, a label for every sample and
# all samples scaled between 0 & 1

# assign two labels to the two rock types: gneiss = 0, marl = 1
df_gneiss['label'] = 0
df_marl['label'] = 1

# give new index to df_marl so that it can be appended to df_gneiss
df_marl.index = np.arange(len(df_gneiss), len(df_gneiss)+len(df_marl))

# concatenate df_gneiss & df_marl to get one big dataframe
df_tot = pd.concat((df_gneiss, df_marl), join='outer')

# scale samples between 0 and 1: scaling must be done after concatenation of
# the dataframes, because otherwise the data clusters would overlap.

# scale features between 0 & 1
for feature in df_tot.columns:
    df_tot[feature] = df_tot[feature] / df_tot[feature].max()


# visualization of data after preprocessing
labelsize = 20
pointsize = 80

fig, ax = plt.subplots(figsize=(9, 6))

ax.scatter(df_tot['UCS'], df_tot['SPZ'], color='black', alpha=0.5, s=pointsize)
ax.grid(alpha=0.5)
ax.set_xlabel('UCS [normalized]', size=labelsize)
ax.set_ylabel('tensile strength [normalized]', size=labelsize)
plt.tight_layout()
plt.savefig('unsupervised_normalized.jpg', dpi=600)
plt.close()


###############################################################################
# machine learning: cluster dataset with three different algorithms:
# k-Means (Lloyd, 1982);
# MeanShift (Fukunaga and Hostetler, 1975) see also (Comaniciu and Meer, 2002);
# AgglomerativeClustering;
# all algorithms are implemented with scikit learn (Pedregosa et al., 2011)

np.random.seed(0)  # fix random seed for reproducibility
data = df_tot.sample(frac=1)  # shuffle data


clfs = [KMeans(n_clusters=2),
        MeanShift(bandwidth=0.33),
        AgglomerativeClustering(n_clusters=2)]

for clf in clfs:

    algo_name = str(clf).split('(')[0]

    features = ['UCS', 'SPZ']
    clf.fit(data[features].values)

    classification = clf.labels_

    acc = round(accuracy_score(data['label'], classification), 3) * 100

    # flip 0 and 1 to see if bad performance is simply caused by the order of
    # cluster label assignement (would happen to MeanShift)
    if acc < 50:
        classification = 1 - classification
        acc = round(accuracy_score(data['label'], classification), 3) * 100
    print(f'accuracy: {acc}%')

    # visualization of clusters with marked wrong classifications
    fig, ax = plt.subplots(figsize=(9, 6))

    idx_class_gneiss = np.where(classification == 0)[0]
    idx_class_marl = np.where(classification == 1)[0]
    idx_wrong = np.where(classification != data['label'].values)[0]

    ax.scatter(data['UCS'].iloc[idx_class_gneiss],
               data['SPZ'].iloc[idx_class_gneiss],
               color='C0', alpha=1, edgecolor='black', s=pointsize,
               label='classified as gneiss')
    ax.scatter(data['UCS'].iloc[idx_class_marl],
               data['SPZ'].iloc[idx_class_marl],
               color='C1', alpha=1, edgecolor='black', s=pointsize,
               label='classified as marl')
    ax.scatter(data['UCS'].iloc[idx_wrong],
               data['SPZ'].iloc[idx_wrong],
               edgecolors='red', marker='o', facecolors='None',
               s=90, linewidth=3,
               label='wrong classifications')

    ax.grid(alpha=0.5)
    ax.set_xlabel('UCS [normalized]', size=labelsize)
    ax.set_ylabel('tensile strength [normalized]', size=labelsize)
    ax.set_title(f'{algo_name}: accuracy {acc}%', size=labelsize)
    ax.legend(fontsize=15)

    plt.tight_layout()
    plt.savefig(f'unsupervised_{algo_name}.jpg', dpi=600)

'''
References:

Comaniciu, D. and Meer, P. (2002) ‘Mean shift: A robust approach toward feature
space analysis’, IEEE Transactions on Pattern Analysis and Machine
Intelligence, vol. 24, no. 5, pp. 603–619.

Fukunaga, K. and Hostetler, L. (1975) ‘The estimation of the gradient of a
density function, with applications in pattern recognition’,
IEEE Transactions on Information Theory, vol. 21, no. 1, pp. 32–40.

Lloyd, S. (1982) ‘Least squares quantization in PCM’,
IEEE Transactions on Information Theory, vol. 28, no. 2, pp. 129–137.

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel,
O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J.,
Passos, A., Cournapeau, D., Brucher, M., Perrot, M. and Édouard, D. (2011)
‘Scikit-learn: Machine Learning in Python’,
Journal of Machine Learning Research, no. 12, pp. 2825–2830.
'''
