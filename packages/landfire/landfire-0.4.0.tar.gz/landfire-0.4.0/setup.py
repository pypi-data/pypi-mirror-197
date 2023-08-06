# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['landfire', 'landfire.product']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0', 'pydantic>=1.10', 'requests>=2.28.0']

extras_require = \
{'geospatial': ['geojson>=3.0.0', 'geopandas>=0.12.0', 'fiona>=1.9.0']}

setup_kwargs = {
    'name': 'landfire',
    'version': '0.4.0',
    'description': 'Landfire',
    'long_description': '# landfire-python\n\n[![PyPI](https://img.shields.io/pypi/v/landfire.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/landfire.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/landfire)][python version]\n[![License](https://img.shields.io/pypi/l/landfire)][license]\n\n[![Read the documentation at https://landfire-python.readthedocs.io/](https://img.shields.io/readthedocs/landfire-python/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/FireSci/landfire-python/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/FireSci/landfire-python/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/landfire/\n[status]: https://pypi.org/project/landfire/\n[python version]: https://pypi.org/project/landfire\n[read the docs]: https://landfire-python.readthedocs.io/\n[tests]: https://github.com/FireSci/landfire-python/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/FireSci/landfire-python\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n`landfire-python` is a wrapper around the [LANDFIRE][landfire] Products Service API, allowing users to obtain any of the available LANDFIRE data layers with just a few lines of code. This library was initially built to faciliate automated data ingest for wildfire modeling and analysis internally at [FireSci][firesci]. However, we\'re happy to open-source and maintain this tool to enable broader user of LANDFIRE data across the wildfire community! 🔥\n\n[landfire]: https://landfire.gov/index.php\n[firesci]: https://firesci.io/\n\n### Supported LANDFIRE functionality\n\n- Clipping requested data to a specific bounding box\n- Reprojection of output data coordinate system to user-specified well-known integer ID format\n- Specifying a list of data product layers and obtaining a multi-band .tif output\n- Modifying the resampling resolution\n\n### Additional functionality\n\n- Search functionality to allow users to search for products by LANDFIRE version, name, product theme, product code, or availability regions (US, AK, HI)\n- Geospatial helpers to obtain suitable bounding box from a GeoJSON polygon or file (GeoJSON, ESRI Shapefile, ESRIJSON, CSV, FlatGeobuf, SQLite)\n- Robust model and enumerations of LANDFIRE products\n- User input validation to reduce potential failed API jobs and server load\n\n### Planned but not currently supported\n\n- Specifying edit rules for fuels data (requires a great deal of user-input validation)\n- Specifying an edit mask for edit rules (requires more LANDFIRE API i/o implementation)\n- Note the LANDFIRE API does not currently provide support for insular regions\n- We will add new products here as they become available\n\n## Requirements\n\n- python >=3.8, <3.12\n- [attrs][attrs], [pydantic][pydantic], and [requests][requests] will be installed when you install the lib\n- Optional dependencies included in the `geospatial` extra are [fiona][fiona], [geojson][geojson] and [geopandas][geopandas]\n\n[attrs]: https://www.attrs.org/en/stable/index.html\n[pydantic]: https://docs.pydantic.dev/\n[requests]: https://requests.readthedocs.io/en/latest/\n[fiona]: https://github.com/Toblerity/Fiona\n[geojson]: https://python-geojson.readthedocs.io/en/latest/#\n[geopandas]: https://geopandas.org/en/stable/\n\n## Installation\n\n```bash\npip install landfire\n```\n\nTo use the geospatial tools found in `geospatial.py`, you\'ll need to install the extra dependencies:\n\n```bash\npip install "landfire[geospatial]"\n```\n\n## Usage\n\nThe simplest possible example requires simply initializing a `Landfire()` object for your area of interest and then submitting a request for data with `request_data()`, specifying the layers of interest and file location to download to (note the file does not need to exist yet, but the path does!).\n\nThis example downloads the minimum required layers to construct a landscape (.lcp) file for FlamMap.\n\n```python\nimport landfire\n\n# Obtain required layers for FlamMap landscape file\nlf = landfire.Landfire(bbox="-107.70894965 46.56799094 -106.02718124 47.34869094")\nlf.request_data(layers=["ELEV2020",   # elevation\n                        "SLPD2020",   # slope degrees\n                        "ASP2020",    # aspect\n                        "220F40_22",  # fuel models\n                        "220CC_22",   # canopy cover\n                        "220CH_22",   # canopy height\n                        "220CBH_22",  # canopy base height\n                        "220CBD_22"], # canopy bulk density\n                output_path="./test_flammap.zip")\n```\n\nPlease see the [documentation][documentation] for further information on possible options, geospatial utilities, and searching for products!\n\n[documentation]: https://landfire-python.readthedocs.io/en/latest/usage.html\n\n## Contributing\n\nContributions are very welcome! 🙏 To learn more, see the [contributor guide][contributor guide].\n\n[contributor guide]: https://landfire-python.readthedocs.io/en/latest/contributing.html\n\n## License\n\nDistributed under the terms of the [MIT license][license], landfire-python is free and open source software.\n\n[license]: https://landfire-python.readthedocs.io/en/latest/license.html\n\n## Issues\n\nIf you encounter any problems, please [file an issue][file an issue] along with a detailed description! 🙌\n\n[file an issue]: https://github.com/FireSci/landfire-python/issues\n\n<!-- github-only -->\n',
    'author': 'FireSci',
    'author_email': 'support@firesci.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/FireSci/landfire-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
