# -*- coding: utf-8 -*-

# This code loads the data that was generated by '00_data_generator.py' and
# and then applies a simple machine learning pipeline to create a machine
# learning model that learns how to separate gneiss from marl according to the
# features tensile strength and unconfined compressive strength

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Perceptron


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
# the dataframes and before a split in train and test data is applied. After
# concatenation because otherwise the data clusters would overlap. Before the
# train test - split because otherwise the train and test data would have
# slightly different scales

# create all positive tensile strength values
df_tot['SPZ'] = df_tot['SPZ'] * -1
shift = df_tot['SPZ'].min() * -1
df_tot['SPZ'] = df_tot['SPZ'].values + shift
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
plt.savefig('supervised_normalized.jpg', dpi=600)
plt.close()

###############################################################################
# train-test split: splitting the whole dataset into two numpy arrays of 20%
# test data and 80% training data.

np.random.seed(0)  # fix random seed for reproducibility

test_size = 0.20  # %
idxs = df_tot.index.values
shuffled_idxs = np.random.permutation(idxs)

test_idxs = shuffled_idxs[:int(len(shuffled_idxs)*test_size)]
train_idxs = shuffled_idxs[int(len(shuffled_idxs)*test_size):]

test_data = df_tot.iloc[test_idxs]
train_data = df_tot.iloc[train_idxs]

features = ['UCS', 'SPZ']

train_X = train_data[features].values
train_y = train_data['label'].values
test_X = test_data[features].values
test_y = test_data['label'].values


# visualization of the train- and test data
fig, ax = plt.subplots(figsize=(9, 6))

ax.scatter(train_data['UCS'], train_data['SPZ'], color='black', alpha=0.5,
           label='train data', s=pointsize)
ax.scatter(test_data['UCS'], test_data['SPZ'], edgecolor='black', color='red',
           alpha=0.8, label='test data', s=pointsize)
ax.grid(alpha=0.5)
ax.set_xlabel('UCS [normalized]', size=labelsize)
ax.set_ylabel('tensile strength [normalized]', size=labelsize)
ax.legend(fontsize=15)
plt.tight_layout()
plt.savefig('supervised_train-test.jpg', dpi=600)
plt.close()


###############################################################################
# machine learning: train a scikit learn implementation of a Perceptron
# (Rosenblatt, 1957) with the training data and test it on the test data.
#
# Rosenblatt, F. (1957) ‘The Perceptron: A Perceiving and Recognizing
# Automaton’, Cornell Aeronatuical Laboratory.

n_epochs = 30  # number of training epochs
clf = Perceptron(max_iter=n_epochs, tol=None)
clf.fit(train_X, train_y)  # training

classification = clf.predict(test_X)  # testing

acc = round(accuracy_score(test_y, classification), 3) * 100
print(f'\n accuracy: {acc}')


# visualization of the results with a mark on wrong classifications
fig, ax = plt.subplots(figsize=(9, 6))

ax.scatter(train_data['UCS'], train_data['SPZ'], color='black', alpha=0.3,
           label='train data', s=pointsize)

idx_class_gneiss = np.where(classification == 0)[0]
idx_class_marl = np.where(classification == 1)[0]
idx_wrong = np.where(test_y != classification)[0]

ax.scatter(test_data['UCS'].iloc[idx_class_gneiss],
           test_data['SPZ'].iloc[idx_class_gneiss],
           color='limegreen', edgecolor='black', alpha=1,
           label='classified as gneiss', s=pointsize)
ax.scatter(test_data['UCS'].iloc[idx_class_marl],
           test_data['SPZ'].iloc[idx_class_marl],
           color='C1', edgecolor='black', alpha=1,
           label='classified as marl', s=pointsize)
ax.scatter(test_data['UCS'].iloc[idx_wrong],
           test_data['SPZ'].iloc[idx_wrong],
           edgecolors='red', marker='o', facecolors='None', s=pointsize+50,
           linewidth=3, label='wrong classifications')

ax.set_title(f'epoch: {n_epochs}, accuracy: {acc}%', size=labelsize)
ax.grid(alpha=0.5)
ax.set_xlabel('UCS [normalized]', size=labelsize)
ax.set_ylabel('tensile strength [normalized]', size=labelsize)
plt.tight_layout()
ax.legend(fontsize=15)
plt.savefig(fr'supervised_epoch{n_epochs}.jpg', dpi=600)
plt.close()