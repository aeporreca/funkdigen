#!/usr/bin/env python3


from argparse import ArgumentParser
from timeit import default_timer


# Types of the data structures we use

Tree        = list[int]
Component   = list[Tree]
Partition   = list[int]
FuncDigraph = list[Component]


# Separator used to flatten components into lists of integers

PREFIX = 0


# Flatten a component (sequence of trees) into a list of integers by
# prefixing the code of each tree by PREFIX

def flatten(C: Component) -> list[int]:
    flattened = []
    for T in C:
        flattened.append(PREFIX)
        flattened += T
    return flattened


# Check if the given component (sequence of trees) is its own minimal
# rotation with respect to lexicographic order. The algorithm is based
# on "Lexicographically least circular substrings" by Kellogg S. Booth
# (Information Processing Letters, 10(4), 1980, pages 240-242) and on
# the errata published at https://www.cs.ubc.ca/~ksbooth/PUB/LCS.shtml

def is_min_rotation(C: Component) -> bool:
    L = flatten(C)
    n = len(L)
    f = [-1] * (2 * n)
    k = 0
    for j in range(1, 2 * n):
        i = f[j - k - 1]
        while i != -1 and L[j % n] != L[(k + i + 1) % n]:
            if L[j % n] < L[(k + i + 1) % n]:
                k = j - i - 1
            i = f[i]
        if i == -1 and L[j % n] != L[(k + i + 1) % n]:
            if L[j % n] < L[(k + i + 1) % n]:
                k = j
            f[j - k] = -1
        else:
            f[j - k] = i + 1
    return L[k:] + L[:k] == L


# Merge a sequence of trees

def merge(trees: list[Tree]) -> Tree:
    assert trees[0] == [1]
    root = sum(T[0] for T in trees)
    merged = [root]
    n = len(trees)
    for i in range(1, n):
        merged += trees[i]
    return merged


# Unmerge a tree into a sequence of trees

def unmerge(T: Tree) -> list[Tree]:
    n = len(T)
    trees = [[1]]
    l = 1
    while l < n:
        r = l + T[l]
        trees.append(T[l:r])
        l = r
    return trees


# Check if a sequence of trees is sorted in lexicographic order

def is_sorted(trees: list[Tree]) -> bool:
    n = len(trees)
    for i in range(n - 1):
        if trees[i] > trees[i + 1]:
            return False
    return True


# Compute the component-unmerge (c-unmerge)

def c_unmerge(C: Component) -> Component | None:
    k = len(C)
    for h in range(k):
        if C[h] != [1]:
            return C[:h] + unmerge(C[h]) + C[h+1:]
    return None


# Compute all merges of a given component

def merges(C: Component) -> list[Component]:
    k = len(C)
    res = []
    for l in range(k - 1):
        for r in range(l + 2, k + 1):
            if C[l] == [1]:
                trees = C[l:r]
                C_lr = C[:l] + [merge(trees)] + C[r:]
                if (is_sorted(C[l:r]) and
                    is_min_rotation(C_lr) and
                    c_unmerge(C_lr) == C):
                    res.append(C_lr)
    return res


# Return the cycle of length n

def cycle(n: int) -> Component:
    return [[1]] * n


# Return the number of vertices of a component

def component_size(C: Component) -> int:
    return sum(len(T) for T in C)


# Compute the next component

def component_successor(C: Component) -> Component:
    merges_C = merges(C)
    if merges_C != []:
        return min(merges_C)
    U = c_unmerge(C)
    while U is not None:
        merges_U = [M for M in merges(U) if M > C]
        if merges_U != []:
            return min(merges_U)
        C = U
        U = c_unmerge(C)
    return cycle(component_size(C) + 1)


# Generate all components (connected functional digraphs) of n vertices

def components(n: int) -> list[Component]:
    if n == 0:
        return []
    result = []
    C = cycle(n)
    while component_size(C) == n:
        result.append(C)
        C = component_successor(C)
    return result


# Return the number of vertices of a functional digraph

def funcdigraph_size(G: FuncDigraph) -> int:
    return sum(component_size(C) for C in G)


# Return the graph consisting of n self-loops

def loops(n: int) -> FuncDigraph:
    return [[[1]]] * n


# Compute the next partition of integer n in lexicographic order, if
# it exists, otherwise the first partition of integer n + 1. The
# algorithm is based on Algorithm 3.1 of "Generating all partitions: A
# comparison of two encodings" by Jerome Kelleher and Barry
# O'Sullivan, https://arxiv.org/abs/0909.2331

def partition_successor(P: Partition) -> Partition:
    n = sum(P)
    if len(P) <= 1:
        return [1] * (n + 1)
    k = len(P) - 1
    P = P + [0] * (n - len(P))
    y = P[k] - 1
    k = k - 1
    x = P[k] + 1
    while x <= y:
        P[k] = x
        y = y - x
        k = k + 1
    P[k] = x + y
    return P[0:k+1]


# Compute the integer partition corresponding to a given functional digraph

def partition(G: FuncDigraph) -> Partition:
    return [component_size(C) for C in G]


# Compute the next functional digraph

def funcdigraph_successor(G: FuncDigraph) -> FuncDigraph:
    m = len(G)
    h = m - 1
    while h >= 0:
        C = component_successor(G[h])
        if component_size(C) == component_size(G[h]):
            result = G[:h] + [C]
            for i in range(h + 1, m):
                if component_size(G[i]) == component_size(C):
                    result.append(C)
                else:
                    result.append(cycle(component_size(G[i])))
            return result
        h = h - 1
    P = partition(G)
    Q = partition_successor(P)
    n = sum(P)
    if sum(Q) == n:
        return [cycle(k) for k in Q]
    else:
        return loops(n + 1)


# Generate all functional digraphs of n vertices

def funcdigraphs(n: int) -> list[FuncDigraph]:
    result = []
    G = loops(n)
    while funcdigraph_size(G) == n:
        result.append(G)
        G = funcdigraph_successor(G)
    return result


# Command line interface

if __name__ == '__main__':
    parser = ArgumentParser(
        description='Generate all functional digraphs up to isomorphism'
    )
    parser.add_argument('size', metavar='size', type=int,
                        help='number of vertices')
    parser.add_argument(
        '-c', '--connected', '--component', action='store_true',
        help='only generate components (connected digraphs)')
    parser.add_argument(
        '-t', '--time', action='store_true',
        help='measure time without printing the generated digraphs')
    args = parser.parse_args()
    n = args.size
    if args.connected:
        generate = components
    else:
        generate = funcdigraphs
    start = default_timer()
    result = generate(n)
    end = default_timer()
    if args.time:
        ndigraphs = len(result)
        print(f'{ndigraphs} digraphs generated in', end=' ')
        time = end - start
        if time < 0.01:
            print(f'{time * 1000:.2f} ms')
        else:
            print(f'{time:.2f} s')
    else:
        for X in result:
            print(X)
