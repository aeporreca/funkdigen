# funkdigen

A generator of functional digraphs up to isomorphism

Based on Antonio E. Porreca, Ekaterina Timofeeva, Polynomial-delay generation of functional digraphs up to isomorphism, arXiv:2302.13832, 2023, https://doi.org/10.48550/arXiv.2302.13832

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
