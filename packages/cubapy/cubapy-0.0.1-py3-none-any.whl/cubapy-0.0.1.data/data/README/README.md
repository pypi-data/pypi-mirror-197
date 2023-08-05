# cubapy

A small library with quadrature/cubature points for unit- lines, 
triangles and tetrahedra for finite element applications.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cubapy:

```bash
pip install cubapy
```

## Usage
There are three functions for cubature: line(p), tri(p), tet(p).
The power p is such that polynomials up to order 2*p are integrated exactly 
as is usually required in finite element software.

```python
from cubapy import *

pts = line(2)
plot_pts(*pts)

pts = tri(3)
plot_pts(*pts)

pts = tet(4)
plot_pts(*pts)
```

## License

cubapy is licensed under [GNU LGPLv3](https://choosealicense.com/licenses/lgpl-3.0).

This library exposes a small wrapper for the [Plotly](https://github.com/plotly/plotly.py) library 
under the [MIT](https://choosealicense.com/licenses/mit/#) license for the purpose of visualization.
