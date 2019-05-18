# -*- coding: utf-8 -*-

# This code loads the data that was generated by '00_data_generator.py' and
# and then creates six scatterplots of the three features.

import matplotlib.pyplot as plt
import pandas as pd


# load into two dataframes

df_gneiss = pd.read_csv('gneiss.csv')
df_marl = pd.read_csv('marl.csv')

# plot data with several scatterplots

fig = plt.figure(figsize=(12, 8))

ax = fig.add_subplot(2, 3, 1)
ax.scatter(df_gneiss['UCS'], df_gneiss['SPZ'], alpha=0.5, color='black')
ax.scatter(df_marl['UCS'], df_marl['SPZ'], alpha=0.5, color='black')
ax.set_xlabel('UCS [MPa]')
ax.set_ylabel('tensile strength [MPa]')
ax.grid(alpha=0.5)

ax = fig.add_subplot(2, 3, 2)
ax.scatter(df_gneiss['DENS'], df_gneiss['UCS'], alpha=0.5, color='black')
ax.scatter(df_marl['DENS'], df_marl['UCS'], alpha=0.5, color='black')
ax.set_xlabel('density [g/cm³]')
ax.set_ylabel('UCS [MPa]')
ax.grid(alpha=0.5)

ax = fig.add_subplot(2, 3, 3)
ax.scatter(df_gneiss['SPZ'], df_gneiss['DENS'], alpha=0.5, color='black')
ax.scatter(df_marl['SPZ'], df_marl['DENS'], alpha=0.5, color='black')
ax.set_xlabel('tensile strength [MPa]')
ax.set_ylabel('density [g/cm³]')
ax.grid(alpha=0.5)

ax = fig.add_subplot(2, 3, 4)
ax.scatter(df_gneiss['UCS'], df_gneiss['SPZ'], alpha=0.5, label='gneiss')
ax.scatter(df_marl['UCS'], df_marl['SPZ'], alpha=0.5, label='marl')
ax.set_xlabel('UCS [MPa]')
ax.set_ylabel('tensile strength [MPa]')
ax.legend()
ax.grid(alpha=0.5)

ax = fig.add_subplot(2, 3, 5)
ax.scatter(df_gneiss['DENS'], df_gneiss['UCS'], alpha=0.5, label='gneiss')
ax.scatter(df_marl['DENS'], df_marl['UCS'], alpha=0.5, label='marl')
ax.set_xlabel('density [g/cm³]')
ax.set_ylabel('UCS [MPa]')
ax.legend()
ax.grid(alpha=0.5)

ax = fig.add_subplot(2, 3, 6)
ax.scatter(df_gneiss['SPZ'], df_gneiss['DENS'], alpha=0.5, label='gneiss')
ax.scatter(df_marl['SPZ'], df_marl['DENS'], alpha=0.5, label='marl')
ax.set_xlabel('tensile strength [MPa]')
ax.set_ylabel('density [g/cm³]')
ax.legend()
ax.grid(alpha=0.5)


plt.tight_layout()
plt.savefig('data.jpg', dpi=600)
