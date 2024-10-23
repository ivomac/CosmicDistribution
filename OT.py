#!/usr/bin/python

import numpy as np
from scipy.optimize import linprog

def find_optimal_transport(C, G, P):

    N = G.shape[0]
    M = np.zeros([N, N])
    for i in range(N):
        for j in range(N):
            M[i, j] = (C[j, 0] - C[i, 1] - G[i, j])*(1-P[i, j])

    K0 = np.kron(np.ones((1, N)), np.identity(N))
    K1 = np.kron(np.identity(N), np.ones((1, N)))
    K = np.vstack([K0, K1])

    d = C[:, 2]
    s = C[:, 3]

    b = np.hstack([s, d])

    Mv = M.reshape(N**2, order='F')

    q = linprog(-Mv, A_ub=K, b_ub=b, method='highs').x
    q = q.reshape((N, N), order='F')

    res = []
    for i in range(N):
        for j in range(N):
            if q[i, j] > 0:
                res.append([i, j, q[i, j]])

    return np.array(res)

if 0:
    C = [[98,100,100,100],
    [98,100,100,100],
    [102,103,100,100],
    [102,103,100,100]]


    G = [[0,1,1,1],
    [1,0,1,1],
    [1,1,0,1],
    [1,1,1,0]]


    P = [[0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]]
elif 0:
    C = [[98,100,100,100],
    [98,100,100,100],
    [102,103,100,100],
    [102,103,100,100],
    [102,103,100,100],]

    G = [[0,1,1,1,1],
    [1,0,1,1,1],
    [1,1,0,1,1],
    [1,1,1,0,1],
    [1,1,1,1,0],]

    P = [[0,0,0.5,0,0],
    [0,0,0,0,0],
    [0.5,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],]
else:
    C = [[98,100,210,170],
    [98,100,100,100],
    [102,103,210,210],
    [102,103,100,100],
    [102,103,100,100],]

    G = [[0,1,1,1,1],
    [1,0,1,1,1],
    [1,1,0,1,1],
    [1,1,1,0,1],
    [1,1,1,1,0],]

    P = [[0,0,0.5,0,0],
    [0,0,0,0,0],
    [0.5,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],]


C = np.array(C)
G = np.array(G)
P = np.array(P)

res = find_optimal_transport(C, G, P)

print(res)
