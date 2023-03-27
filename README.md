# funkdigen

An proof-of-concept generator of functional digraphs (uniform outdegree 1) up to isomorphism, also called mapping patterns, finite (endo)functions, or finite dynamical systems; see sequence [A001372](https://oeis.org/A001372) on the [OEIS](https://oeis.org). It is also possible to only generate *connected* functional digraphs (sequence [A002861](https://oeis.org/A002861) on the OEIS).

> **Warning**
> `funkdigen` is algorithmically efficient, but not efficient in terms of raw execution time, being rather a straightforward implementation of the algorithms in the paper below. If you want efficiency, as well as an output format compatible with other sofware, please use [`funkdigen2`](https://github.com/aeporreca/funkdigen2) instead!


## Background

Based on Antonio E. Porreca, Ekaterina Timofeeva, Polynomial-delay generation of functional digraphs up to isomorphism, arXiv:2302.13832, 2023, https://doi.org/10.48550/arXiv.2302.13832


## Output format

The output format is described in the [paper](https://doi.org/10.48550/arXiv.2302.13832) itself (Definitions 1, 2 and 23, as well as Examples 10 and 25). To summarise, keeping in mind that each connected component of a functional digraph consists of directed trees (with arcs pointing towards the root) with roots arranged along a limit cycle:

- Each functional digraph code is a list of the codes of its connected components in the lexicographic order induced by the algorithm for generating them.
- Each connected functional digraph code is the lexicographically minimal rotation of the list of the codes of its trees.
- The code of a tree $T$ is the list obtained by concatenating $[n]$ with $t_1, \ldots, t_k$, where $[n]$ is the singleton list containing the number $n$ of nodes of $T$, and $t_1, \ldots, t_k$ are the codes (computed recursively) of its immediate subtrees in lexicographic order.


## Installation

Just download the code from the [Releases](https://github.com/aeporreca/funkdigen/releases) page (or clone this repository if you want the latest changes). Python 3.9 is needed in order to run `funkdigen`.


## Usage

```
usage: funkdigen.py [-h] [-c] [-q] [-V] size

Generate all functional digraphs up to isomorphism

positional arguments:
  size             number of vertices

options:
  -h, --help       show this help message and exit
  -c, --connected  only generate connected digraphs
  -q, --quiet      do not print the generated digraphs
  -V, --version    show program's version number and exit
```


## Authors and license

The `funkdigen2` software is copyright © 2023 by [Antonio E. Porreca](https://aeporreca.org) and [Ekaterina Timofeeva](https://www.linkedin.com/in/ektim239), and its source code is distributed under the GNU GPL 3.0 license.
