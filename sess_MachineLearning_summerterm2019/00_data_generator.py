# -*- coding: utf-8 -*-

# This code generates two clusters of synthetic rock mechanical data.
# Two common rock types are chosen: gneiss and marl. The data is then saved as
# a .csv file for further usage

import numpy as np
import pandas as pd


# the statistical values of the two rock types are based on experience and are
# not associated with any specific project.
# Statistical values comprise the unconfined compressive strength (UCS),
# tensile strength (SPZ) and density (DENS) of the rocks.

gneiss = {'meanUCS': 94.5, 'stdUCS': 50,
          'meanSPZ': 9.5, 'stdSPZ': 4.35,
          'meanDENS': 2.77, 'stdDENS': 0.118}

marl = {'meanUCS': 4.86, 'stdUCS': 8.5,
        'meanSPZ': 2, 'stdSPZ': 2.2,
        'meanDENS': 2.29, 'stdDENS': 0.14}


np.random.seed(7)  # fix random seed for reproducibility


# 350 data points are generated for the gneiss and 175 for the marl
size = 350

UCS_gneiss = np.absolute(np.random.normal(gneiss['meanUCS'],
                                          gneiss['stdUCS'], size))
SPZ_gneiss = np.absolute(np.random.normal(gneiss['meanSPZ'],
                                          gneiss['stdSPZ'], size))
DENS_gneiss = np.absolute(np.random.normal(gneiss['meanDENS'],
                                           gneiss['stdDENS'], size))

UCS_marl = np.absolute(np.random.normal(marl['meanUCS'],
                                        marl['stdUCS'], int(size/2)))
SPZ_marl = np.absolute(np.random.normal(marl['meanSPZ'],
                                        marl['stdSPZ'], int(size/2)))
DENS_marl = np.absolute(np.random.normal(marl['meanDENS'],
                                         marl['stdDENS'], int(size/2)))

df_gneiss = pd.DataFrame({'UCS': UCS_gneiss,
                          'SPZ': SPZ_gneiss,
                          'DENS': DENS_gneiss})
df_marl = pd.DataFrame({'UCS': UCS_marl,
                        'SPZ': SPZ_marl,
                        'DENS': DENS_marl})

df_gneiss.to_csv('gneiss.csv', index=False)
df_marl.to_csv('marl.csv', index=False)
