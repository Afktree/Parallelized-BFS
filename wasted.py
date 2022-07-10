import mpi4py
import numpy as np
import queue
from mpi4py import MPI


def createGraph(n):  # directed graph
    res = np.random.randint(2, size=(n, n))
    return res ^ res.T


def bfs(adj, n):
    res = np.empty(n, dtype=int)
    q = queue.Queue()
    q.put(0)
    visited = np.array([False for i in range(n)])
    visited[0] = True
    ind = 0
    while not q.empty():
        u = q.get()
        res[ind] = u
        ind += 1
        for i in range(n):
            if adj[u][i] > 0 and visited[i] == False:
                q.put(i)
                visited[i] = True
    return res


def div(arr):
    return arr[:len(arr)//2], arr[len(arr)//2:]


if __name__ == "__main__":

    nVertices = 10

    comm = MPI.COMM_WORLD
    nProcs = comm.Get_size()
    rank = comm.Get_rank()
    if rank == 0:
        adj_mat = createGraph(nVertices)
        s1, s2 = div(adj_mat)
        comm.send(s2, 4)
        s1, s2 = div(s1)
        comm.send(s2, 2)
        s1, s2 = div(s1)
        comm.send(s2, 1)

        lst = []
        for i in range(len(s1)):
            if s1[i] == 1:
                lst.append(i)

        part_sum = comm.recv(source=1)
        for i in range(len(part_sum)):
            if part_sum[i] not in lst:
                lst.append(part_sum[i])
        part_sum2 = comm.recv(source=2)
        for i in range(len(part_sum2)):
            if part_sum2[i] not in lst:
                lst.append(part_sum2[i])
        part_sum3 = comm.recv(source=4)
        for i in range(len(part_sum3)):
            if part_sum3[i] not in lst:
                lst.append(part_sum3[i])

        print(lst)

    if rank == 1:
        lst = []
        s1 = comm.recv(source=0)
        for i in range(len(s1)):
            if s1[i] == 1:
                lst.append(i)
        comm.send(lst, 0)

    if rank == 2:
        s1 = comm.recv(source=0)
        s1, s2 = div(s1)
        comm.send(s2, 3)
        for i in range(len(s1)):
            if s1[i] == 1:
                lst.append(i)

        part_list = comm.recv(source=3)
        for i in range(len(part_list)):
            if part_list[i] not in lst:
                lst.append(i)

        comm.send(lst, 0)

    if rank == 3:
        lst = []
        s1 = comm.recv(source=2)
        for i in range(len(s1)):
            if s1[i] == 1:
                lst.append(i)
        comm.send(lst, 2)

    if rank == 4:
        lst = []
        s1 = comm.recv(source=0)
        s1, s2 = div(s1)
        comm.send(s2, 6)
        s1, s2 = div(s1)
        comm.send(s2, 5)

        for i in range(len(s1)):
            if s1[i] == 1:
                lst.append(i)

        part_sum = comm.recv(source=5)
        for i in range(len(part_sum)):
            if part_sum[i] not in lst:
                lst.append(part_sum[i])
        part_sum2 = comm.recv(source=6)
        for i in range(len(part_sum2)):
            if part_sum2[i] not in lst:
                lst.append(part_sum2[i])
        comm.send(lst, 0)

    if rank == 5:
        lst = []
        s1 = comm.recv(source=4)
        for i in range(len(s1)):
            if s1[i] == 1:
                lst.append(i)
        comm.send(lst, 4)

    if rank == 6:
        s1 = comm.recv(source=4)
        s1, s2 = div(s1)
        comm.send(s2, 7)
        for i in range(len(s1)):
            if s1[i] == 1:
                lst.append(i)

        part_list = comm.recv(source=7)
        for i in range(len(part_list)):
            if part_list[i] not in lst:
                lst.append(i)

        comm.send(lst, 4)

    if rank == 7:
        lst = []

        rec = comm.recv(source=6)
        print(rec)
        for s1 in rec:
            for i in range(len(s1)):

                if i not in lst and s1[i] == 1:
                    lst.append(i)
        print(lst, rank)
        comm.send(lst, 6)
