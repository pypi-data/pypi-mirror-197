#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 22:54:06 2023

@author: Ioannis Nicolis
"""

import numpy as np
from numpy.linalg import svd

class CA:
    """
    Correspondence Analysis (CA) class.
    ...
    Attributes
    ----------
    columnCoords : numpy array
               The column coordinates
    rowCoords : numpy array
               The row coordinates
    """

    def __init__(self, df):
        """
        Parameters
        __________
        df : numpy array
           Contingency table to be analysed
        """

        N = df.sum() # Total size
        P = df/N # Frequencies
        f_idot = P.sum(axis=1, keepdims=True) # line margins
        f_dotj = P.sum(axis=0, keepdims=True) # column margins
        D_I = np.diagflat(f_idot) # line margins diagonal matrix
        D_J = np.diagflat(f_dotj) # column margins diagonal matrix
        D_Iinv = np.diagflat(1/f_idot) # line margins diagonal matrix inverse
        D_Jinv = np.diagflat(1/f_dotj) # column margins diagonal matrix inverse
        P0 = D_Iinv@P-np.ones_like(P)@D_J # line coords in column space
        H = np.sqrt(D_Jinv)@P0.transpose()@D_I@P0@np.sqrt(D_Jinv)
        U,Lambda,V = svd(H)
        A = np.sqrt(D_Jinv)@U@np.sqrt(np.diag(Lambda)) # Column coordinates
        C = P0@np.sqrt(D_Jinv)@U # Row coordinates
        self.columnCoords = A
        self.rowCoords = C
