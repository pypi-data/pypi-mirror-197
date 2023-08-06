# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fibsem_tools', 'fibsem_tools.io', 'fibsem_tools.metadata']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.10.0,<2.0.0',
 'distributed>=2021.10.0',
 'fsspec>=2022.2.0',
 'h5py>=3.1.0,<4.0.0',
 'mrcfile>=1.2.0,<2.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pint>=0.20.1,<0.21.0',
 'pydantic-ome-ngff>=0.2.0,<0.3.0',
 'pydantic>=1.8.2,<2.0.0',
 's3fs>=2022.2.0',
 'tensorstore>=0.1.8,<0.2.0',
 'xarray-ome-ngff>=1.2.0,<2.0.0',
 'xarray>=2022.03.0',
 'zarr>=2.10.3,<3.0.0']

setup_kwargs = {
    'name': 'fibsem-tools',
    'version': '1.3.0',
    'description': 'Tools for processing FIBSEM datasets',
    'long_description': 'None',
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
