import numpy as np
from bfs import bfs
import time


def createGraph(n):  # directed graph
    res = np.random.randint(2, size=(n, n))
    return res ^ res.T


def adjacent_nodes(adj_mat, x):
    idx_lst = []
    adj_list = adj_mat[x]
    for idx, val in enumerate(adj_list):
        if val == 1:
            idx_lst.append(idx)
    return idx_lst


def get_neighbours(cq, adj_mat, visited, key):
    split = cq
    found = False
    nq = []
    # if rank == 1:
    #     print(1)
    for u in split:
        for v in adjacent_nodes(adj_mat, u):
            if v == key:
                found = True
            if visited[v] == np.inf:
                visited[v] = u
                nq.append(v)

    return nq, found, visited


def parallelbfs(adj_mat, key):
    root = 0
    curr_que = []
    visited = []
    for i in range(len(adj_mat)):
        visited.append(np.inf)
    visited[root] = 0
    curr_que.append(root)

    while curr_que:

        new_que, found, visited = get_neighbours(
            curr_que, adj_mat, visited, key)
        if found:
            return 1

        curr_que = new_que

    return 0


def start1():

    nVertices = 1000
    adj_mat = None

    adj_mat = createGraph(nVertices)
    # adj_mat = [[0, 1, 0, 0],
    #            [1, 0, 0, 0],
    #            [0, 0, 0, 0],
    #            [0, 0, 0, 0]]

    # sending same matrix to all processors

    t1 = time.time()
    key = 5

    flag = parallelbfs(adj_mat, key)

    if flag == 1:
        print("Node Found")

    else:
        print("Node not Found")

    t2 = time.time()
    print("time take by serial code:", t2-t1)


if __name__ == "__main__":

    start1()
