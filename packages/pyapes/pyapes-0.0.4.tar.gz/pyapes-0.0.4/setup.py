# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyapes',
 'pyapes.core',
 'pyapes.core.geometry',
 'pyapes.core.mesh',
 'pyapes.core.solver',
 'pyapes.core.variables',
 'pyapes.testing']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0',
 'pymytools>=0.1.0,<0.2.0',
 'tensorboard>=2.12.0,<3.0.0',
 'torch>=1.13.1,<2.0.0']

setup_kwargs = {
    'name': 'pyapes',
    'version': '0.0.4',
    'description': 'Python Awesome Partial differential Equation Solver',
    'long_description': '\n# THIS LIBRARY IS CURRENTLY WIP (LIMITED FEATURES ARE AVAILABLE)!! IT IS BETA STAGE\n\n# pyapes\n\n**PY**thon **A**wesome **P**artial differential **E**quation **S**olver (general purpose finite difference PDE solver)\n\n![python](http://ForTheBadge.com/images/badges/made-with-python.svg)\n\n## Description\n\n`pyapes` is designed to solve various engineering problems in rectangular grid.\n\nThe goal of `pyapes` (should be/have) is\n\n- Cross-platform\n  - Both tested on Mac and Linux (Arch)\n  - Windows support is under testing\n- GPU acceleration in a structured grid with [PyTorch](https://pytorch.org)\n  - Use of `torch.Tensor`. User can choose either `torch.device("cpu")` or `torch.device("cuda")`.\n- Generically expressed (OpenFOAM-like, human-readable formulation)\n\n## Installation\n\nWe recommend to use `poetry` to manage/install all dependencies.\n\n- From `git`\n\n  ```bash\n  git clone git@gitlab.ethz.ch:kchung/pyapes.git\n  cd pyapes\n  poetry install\n  ```\n\n- From `pypi`\n\n  ```bash\n  python3 -m pip install pyapes\n  # or\n  poetry add pyapes\n  ```\n\n## Dependencies\n\n- Core dependency\n  - `python >= 3.10`\n    - As of 19.02.2023, `torch` does not support 3.11 properly (for the official release). Therefore, stick to `python3.10`.\n  - `numpy >= 1.21.0`\n  - `torch >= 1.10.0`\n  - `pyevtk >= 1.2.0`\n  - `tensorboard >= 2.7.0`\n- Misc dependency (Aesthetic)\n  - `tqdm >= 4.62.3`\n  - `rich >= 10.12.0`\n\n## Implemented Features\n\n- CPU/GPU computation using `torch`\n- FDM Discretizations\n  - Spatial: `Grad`, `Laplacian`, `Div`\n    - Supports flux limiter `upwind` for the `Div` operator\n  - Temporal: `Ddt`\n- Boundary conditions:\n  - Supports `Dirichlet`, `Neumann`, `Periodic`, and `Symmetry`\n- Testing and demonstration\n  - `Mesh`, `Field`, `FDM`\n  - `Solver`\n    - The Poisson equation\n    - The advection-diffusion equation\n\n## Examples\n\nCheck our [demos files](demos/)\n\n## Todos\n\n- Boundary conditions\n  - [ ] Inflow/Outflow\n- Need different derivative order at the cell face\n  - Additional features\n    - [ ] High order time discretization\n    - [ ] Immersed body BC\n    - [ ] Higher order flux limiters (`quick`)\n- Testing and validation\n  - [ ] `Ddt` class (implementation is tested but haven\'t validated with practical test cases)\n- Working on demo files\n  - [x] The Poisson equation\n  - [x] The advection-diffusion equation\n  - [ ] The Burgers\' equation\n  - [ ] The Navier-Stokes equation at low Reynolds numbers\n  - [ ] The Black-Scholes equation\n',
    'author': 'Kyoungseoun Chung',
    'author_email': 'kchung@student.ethz.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
