# funkdigen

An proof-of-concept generator of functional digraphs (uniform outdegree 1) up to isomorphism, also called mapping patterns, finite (endo)functions, or finite dynamical systems; see sequence [A001372](https://oeis.org/A001372) on the [OEIS](https://oeis.org). It is also possible to only generate *connected* functional digraphs (sequence [A002861](https://oeis.org/A002861) on the OEIS).

## Background

Based on Antonio E. Porreca, Ekaterina Timofeeva, Polynomial-delay generation of functional digraphs up to isomorphism, arXiv:2302.13832, 2023, https://doi.org/10.48550/arXiv.2302.13832

## Output format

The output format is described in the [paper](https://doi.org/10.48550/arXiv.2302.13832) itself (Definitions 1, 2 and 23, as well as Examples 10 and 25). To summarise, keeping in mind that each connected component of a functional digraph consists of directed trees (with arcs pointing towards the root) with roots arranged along a limit cycle:

- Each functional digraph code is a list of the codes of its connected components in the lexicographic order induced by the algorithm for generating them.
- Each connected functional digraph code is the lexicographically minimal rotation of the list of the codes of its trees.
- The code of a tree $T$ is the list obtained by concatenating $[n]$ with $t_1, \ldots, t_k$, where $[n]$ is the singleton list containing the number $n$ of nodes of $T$, and $t_1, \ldots, t_k$ are the codes (computed recursively) of its immediate subtrees in lexicographic order.

## Usage

```
usage: funkdigen.py [-h] [-c] [-t] size

Generate all functional digraphs up to isomorphism

positional arguments:
  size                  number of vertices

options:
  -h, --help            show this help message and exit
  -c, --connected, --component
                        only generate components (connected digraphs)
  -t, --time            measure time without printing the generated digraphs
```
