# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tjax',
 'tjax._src',
 'tjax._src.dataclasses',
 'tjax._src.display',
 'tjax._src.fixed_point',
 'tjax._src.gradient']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.4.6',
 'numpy>=1.22',
 'optax>=0.1',
 'rich>=12.6',
 'typing_extensions>=4.2']

setup_kwargs = {
    'name': 'tjax',
    'version': '0.28.3',
    'description': 'Tools for JAX.',
    'long_description': '=============\nTools for JAX\n=============\n\n.. role:: bash(code)\n    :language: bash\n\n.. role:: python(code)\n    :language: python\n\nThis repository implements a variety of tools for the differential programming library\n`JAX <https://github.com/google/jax>`_.\n\n----------------\nMajor components\n----------------\n\nTjax\'s major components are:\n\n- A `dataclass <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/dataclasses>`_ decorator :python:`dataclasss` that facilitates defining structured JAX objects (so-called "pytrees"), which benefits from:\n\n  - the ability to mark fields as static (not available in `chex.dataclass`), and\n  - a display method that produces formatted text according to the tree structure.\n\n- A `fixed_point <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/fixed_point>`_ finding library heavily based on `fax <https://github.com/gehring/fax>`_.  Our\n  library\n\n  - supports stochastic iterated functions, and\n  - uses dataclasses instead of closures to avoid leaking JAX tracers.\n\n- A `shim <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/gradient>`_ for the gradient transformation library `optax <https://github.com/deepmind/optax>`_ that supports:\n\n\n  - easy differentiation and vectorization of “gradient transformation” (learning rule) parameters,\n  - gradient transformation objects that can be passed *dynamically* to jitted functions, and\n  - generic type annotations.\n\n- A pretty printer :python:`print_generic` for aggregate and vector types, including dataclasses.  (See\n  `display <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/display>`_.)  It features:\n\n  - a version for printing traced values :python:`tapped_print_generic`,\n  - decoding size of the batched axes when printing ordinary and traced values,\n  - colorized tree output for aggregate structures, and\n  - formatted tabular output for arrays (or statistics when there\'s no room for tabular output).\n\n----------------\nMinor components\n----------------\n\nTjax also includes:\n\n- Versions of :python:`custom_vjp` and :python:`custom_jvp` that support being used on methods:\n  :python:`custom_vjp_method` and :python:`custom_vjp_method`\n  (See `shims <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/shims.py>`_.)\n\n- Tools for working with cotangents.  (See\n  `cotangent_tools <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/cotangent_tools.py>`_.)\n\n- JAX tree registration for `NetworkX <https://networkx.github.io/>`_ graph types.  (See\n  `graph <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/graph.py>`_.)\n\n- Leaky integration :python:`leaky_integrate` and Ornstein-Uhlenbeck process iteration\n  :python:`diffused_leaky_integrate`.  (See `leaky_integral <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/leaky_integral.py>`_.)\n\n- An improved version of :python:`jax.tree_util.Partial`.  (See `partial <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/partial.py>`_.)\n\n- A testing function :python:`assert_tree_allclose` that automatically produces testing code.  And, a related\n  function :python:`tree_allclose`.  (See `testing <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/testing.py>`_.)\n\n- Basic tools like :python:`divide_where`.  (See `tools <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/tools.py>`_.)\n\n-----------------------\nContribution guidelines\n-----------------------\n\n- Conventions: PEP8.\n\n- How to run tests: :bash:`pytest .`\n\n- How to clean the source:\n\n  - :bash:`ruff .`\n  - :bash:`pyright`\n  - :bash:`mypy`\n  - :bash:`isort .`\n  - :bash:`pylint tjax tests`\n',
    'author': 'Neil Girdhar',
    'author_email': 'mistersheik@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NeilGirdhar/tjax',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
