import numpy as np
import queue
import time


def createGraph(n):  # directed graph
    # returns file handle
    with open("/Users/srich/OneDrive/Desktop/sest.txt", "r") as file:
        file.read()
    for i in file:
        print(i)


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


if __name__ == "__main__":
    t1 = time.time()
    nVertices = 10
    adj_mat = createGraph(nVertices)
    res = bfs(adj_mat, nVertices)
    print(res[:10])
    t2 = time.time()
    print(t2-t1)
