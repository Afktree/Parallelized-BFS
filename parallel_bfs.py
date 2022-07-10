import numpy as np
from bfs import bfs
from mpi4py import MPI
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


def get_neighbours(cq, adj_mat, visited, key, comm, nProcs, rank):
    split = np.array_split(cq, nProcs)
    split = comm.scatter(split, root=0)
    found = False
    nq = []

    for u in split:
        for v in adjacent_nodes(adj_mat, u):
            if v == key:
                found = True
            if visited[v] == np.inf:
                visited[v] = u
                nq.append(v)
    res = comm.reduce(nq, root=0, op=MPI.SUM)
    if rank == 0:
        return res, found, visited


def parallelbfs(adj_mat, comm, nProcs, rank, key):
    root = 0
    curr_que = []
    visited = []
    for i in range(len(adj_mat)):
        visited.append(np.inf)
    visited[root] = 0
    curr_que.append(root)

    while curr_que:
        if rank == 0:
            new_que, found, visited = get_neighbours(
                curr_que, adj_mat, visited, key, comm, nProcs, rank)
            if found:
                return 1

            curr_que = new_que
        else:
            get_neighbours(curr_que, adj_mat, visited, key, comm, nProcs, rank)

    if rank == 0:
        return 0
    else:
        return -1


def start1(comm, rank, nProcs):

    start_time = MPI.Wtime()

    nVertices = 100
    adj_mat = None

    if rank == 0:

        adj_mat = createGraph(nVertices)
        # adj_mat = [[0, 1, 0, 0],
        #            [1, 0, 0, 0],
        #            [0, 0, 0, 0],
        #            [0, 0, 0, 0]]

    # sending same matrix to all processors
    adj_mat = comm.bcast(adj_mat, root=0)

    key = 56

    flag = parallelbfs(adj_mat, comm, nProcs, rank, key)
    end_time = MPI.Wtime()
    if flag == 1:
        print("key =", key, "Node Found")

    else:
        print("key =", key, "Node not Found")
    print("time taken by parallel process", end_time-start_time)


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nProcs = comm.Get_size()

    start1(comm, rank, nProcs)
