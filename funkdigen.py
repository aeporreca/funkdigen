#!/usr/bin/env python3

# funkdigen
# Copyright (C) 2024 Antonio E. Porreca, Ekaterina Timofeeva

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# A generator of functional digraphs up to isomorphism. Based on
# Antonio E. Porreca, Ekaterina Timofeeva, Polynomial-delay generation
# of functional digraphs up to isomorphism, arXiv:2302.13832, 2023,
# https://doi.org/10.48550/arXiv.2302.13832


from argparse import ArgumentParser
from timeit import default_timer
from sys import stderr


# Generic code for reverse search

def generate(fst):
    i = 0
    cur = fst
    dep = 0
    while cur != fst or i < nchildren(cur):
        while i < nchildren(cur):
            nxt = child(cur, i)
            i = i + 1
            if nxt is not None:
                par = parent(nxt)
                if par == cur:
                    cur = nxt
                    dep = 1 - dep
                    if dep == 0:
                        yield cur
                    i = 0
        if cur != fst:
            if dep == 1:
                yield cur
            i = backtrack(cur) + 1
            cur = parent(cur)
            dep = 1 - dep


# Code for computing the successor

def successor(sol):
    dep = depth(sol)
    if dep == 0:
        return (first_grandchild(sol) or
                first_child(sol) or
                next_sibling(sol) or
                parent(sol))
    else:
        return (next_niece(sol) or
                next_sibling(sol) or
                next_aunt(sol) or
                grandparent(sol))


def first_child(sol):
    i = 0
    while i < nchildren(sol):
        cld = child(sol, i)
        if cld is not None:
            par = parent(cld)
            if par == sol:
                return cld
        i = i + 1
    return None


def first_grandchild(sol):
    cld = first_child(sol)
    if cld is None:
        return None
    return first_child(cld)


def next_sibling(sol):
    par = parent(sol)
    if par is None:
        return None
    i = backtrack(sol) + 1
    while i < nchildren(par):
        sib = child(par, i)
        if sib is not None:
            par2 = parent(sib)
            if par2 == par:
                return sib
        i = i + 1
    return None


def next_aunt(sol):
    par = parent(sol)
    if par is None:
        return None
    return next_sibling(par)


def next_niece(sol):
    sib = next_sibling(sol)
    if sib is None:
        return None
    return first_child(sib)


def grandparent(sol):
    par = parent(sol)
    if par is None:
        return None
    return parent(par)
        

# Problem-specific code

def first(n):
    return [[1]] * n


def nchildren(C):
    k = len(C)
    return 2 * (k - 1)


def child(C, i):
    k = len(C)
    if i < k - 1:
        D = C[:i] + [merge(C[i], C[i+1])] + C[i+2:]
        if is_valid_comp(D):
            return D
    elif k - 1 <= i < 2 * (k - 1):
        j = i - (k - 1)
        if C[j] != C[j+1]:
            D = C[:j] + [merge(C[j+1], C[j])] + C[j+2:]
            if is_valid_comp(D):
                return D
    return None


def parent(C):
    k = len(C)
    for i in range(k):
        if C[i] != [1]:
            T1, T2 = unmerge(C[i])
            if T1 <= T2:
                D = C[:i] + [T1, T2] + C[i+1:]
            else:
                D = C[:i] + [T2, T1] + C[i+1:]
            return D


def backtrack(C):
    k = len(C)
    for i in range(k):
        if C[i] != [1]:
            T1, T2 = unmerge(C[i])
            if T1 <= T2:
                return i
            else:
                return i + k


def depth(C):
    d = sum(len(T) for T in C) - len(C)
    return d % 2


# Auxiliary code

def is_sorted(A):
    n = len(A)
    for i in range(n - 1):
        if A[i] > A[i + 1]:
            return False
    return True


def subtrees(T):
    n = len(T)
    trees = []
    l = 1
    while l < n:
        r = l + T[l]
        trees.append(T[l:r])
        l = r
    return trees


def is_valid_tree(T):
    n = len(T)
    if T[0] != n:
        return False
    subs = subtrees(T)
    for S in subs:
        if not is_valid_tree(S):
            return False
    return is_sorted(subs)


def is_min_rotation(A):
    # Naive implementation
    n = len(A)
    for i in range(1, n):
        if A[i:] + A[:i] < A:
            return False
    return True


def is_valid_comp(C):
    for T in C:
        if not is_valid_tree(T):
            return False
    return is_min_rotation(C)


def merge(T1, T2):
    return [T1[0] + T2[0]] + T1[1:] + T2


def unmerge(T):
    assert T != [1]
    # Find the last subtree
    n = len(T)
    i = 1
    while i + T[i] < n:
        i += T[i]
    T2 = T[i:]
    T1 = [T[0] - T2[0]] + T[1:i]
    return T1, T2


def partitions(n):
    # Algorithm by Jerome Kelleher, Barry O'Sullivan
    # https://arxiv.org/pdf/0909.2331
    if n == 0:
        yield []
        return
    a = [0] * (n + 1)
    k = 1
    a[1] = n
    while k != 0:
        y = a[k] - 1
        k = k - 1
        x = a[k] + 1
        while x <= y:
            a[k] = x
            y = y - x
            k = k + 1
        a[k] = x + y
        yield a[:k+1]


# Generation of functional digraphs

def components(n):
    if n == 0:
        return 0
    F = first(n)
    if not args.quiet:
        print(f'[F]')
    count = 1
    for C in generate(F):
        count += 1
        if not args.quiet:
            print(f'[{C}]')
    return count


def funcdigraphs(n):
    count = 0
    for part in partitions(n):
        G = [first(i) for i in part]
        count += 1
        if not args.quiet:
            print(G)
        m = len(G)
        found = True
        while found:
            found = False
            for i in reversed(range(m)):
                D = successor(G[i])
                if D is not None:
                    found = True
                    G[i] = D
                    for j in range(i+1, m):
                        if part[j] == part[i]:
                            G[j] = D
                        else:
                            G[j] = first(part[j])
                    count += 1
                    if not args.quiet:
                        print(G)
                    break
    return count


# Command-line interface

parser = ArgumentParser(
    description='Generate all functional digraphs up to isomorphism'
)
parser.add_argument(
    'size', metavar='size', type=int, help='number of vertices'
)
parser.add_argument(
    '-c', '--connected', action='store_true',
    help='only generate connected digraphs'
)
parser.add_argument(
    '-q', '--quiet', action='store_true',
    help='do not print the generated digraphs'
)
parser.add_argument(
    '-V', '--version', action='version', version='%(prog)s 1.2'
)
args = parser.parse_args()
n = args.size
start = default_timer()
if args.connected:
    count = components(n)
else:
    count = funcdigraphs(n)
end = default_timer()
time = end - start
print(f'{count} digraphs generated in {time:.2f} s', file=stderr)
