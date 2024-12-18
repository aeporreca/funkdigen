> [!WARNING]
> `funkdigen`, although efficient from an asymptotic point of view, is not efficient in terms of raw execution time, being rather a straightforward implementation in Python of the algorithms described in the the paper below. If you want _real_ efficiency, as well as an output format compatible with [established software](https://pallini.di.uniroma1.it), please use [`funkdigen2`](https://aeporreca.org/funkdigen2) instead! 🙂


# funkdigen

An proof-of-concept generator of functional digraphs (uniform outdegree 1) up to isomorphism, also called mapping patterns, finite (endo)functions, or finite dynamical systems; see sequence [A001372](https://oeis.org/A001372) on the [OEIS](https://oeis.org). It is also possible to only generate *connected* functional digraphs (sequence [A002861](https://oeis.org/A002861) on the OEIS).


## Background

Based on Oscar Defrain, Antonio E. Porreca, Ekaterina Timofeeva, Polynomial-delay generation of functional digraphs up to isomorphism, _Discrete Applied Mathematics_ 357, 24–33, 2024, https://doi.org/10.1016/j.dam.2024.05.030


## Output format

The output format is described in the [paper](https://doi.org/10.1016/j.dam.2024.05.030) itself. To summarise, keeping in mind that each connected component of a functional digraph consists of directed trees (with arcs pointing towards the root) with roots arranged along a limit cycle:

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


## Credits

The `funkdigen` software is copyright © 2024 by [Oscar Defrain](https://pageperso.lis-lab.fr/oscar.defrain/), [Antonio E. Porreca](https://aeporreca.org) and [Ekaterina Timofeeva](https://www.linkedin.com/in/ektim239), and its source code is distributed under the GNU GPL 3.0 license. The development has been partly funded by the French [ANR](https://anr.fr) projet [FANs ANR-18-CE40-0002 (Foundations of Automata Networks)](http://sylvain.sene.pages.lis-lab.fr/fans/).
