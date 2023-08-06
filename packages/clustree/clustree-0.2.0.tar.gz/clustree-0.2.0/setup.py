# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['clustree']

package_data = \
{'': ['*']}

install_requires = \
['igraph>=0.10.4,<0.11.0',
 'matplotlib>=3.6,<4.0',
 'networkx>=3,<4',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'pairing-functions==0.2.1',
 'pandas>=1.5,<2.0']

setup_kwargs = {
    'name': 'clustree',
    'version': '0.2.0',
    'description': 'Visualize relationship between clusterings at different resolutions',
    'long_description': '# clustree\n\n## Status\n\n**Functionality: Implemented**\n\n* Directed graph representing clustree. Nodes are parsed images and node information is encoded by a border surrounding the image.\n* Loading: Data provided directly or through a path to parent directory. Images provided through a path to parent directory.\n* Appearance: Edge and node color can correspond to one of: #samples that pass through edge/node, cluster resolution `K`, or a fixed color. In the case of node color, a column name in the data and aggregate function can be used too. Use of column name and #samples creates a continuous colormap, whilst the other options result in discrete colors.\n* Layout: Reingold-Tilford algorithm used for node positioning. Not recommended for kk > 12 due to memory bottleneck in igraph dependency.\n* Legend: demonstration of node / edge color.\n\n\n**Functionality: To Add**\n\n* Legend: demonstration of transparency of edges.\n* Layout: Bespoke implementation of Reingold-Tilford algorithm to overcome dependency\'s memory bottleneck.\n\n## Usage\n\n### Installation\n\nInstall the package with pip:\n\n```\npip install clustree\n```\n\n### Quickstart\n\nThe powerhouse function of the library is `clustree`. Use\n\n```\nfrom clustree import clustree\n```\n\nto import the function. A detailed description of the parameters is provided below.\n\n```\ndef clustree(\n    data: Union[Path, str],\n    prefix: str,\n    images: Union[Path, str],\n    output_path: Optional[Union[Path, str]] = None,\n    draw: bool = True,\n    node_color: str = "prefix",\n    node_color_aggr: Optional[Union[Callable, str]] = None,\n    node_cmap: Union[mpl.colors.Colormap, str] = "inferno",\n    edge_color: str = "samples",\n    edge_cmap: Union[mpl.colors.Colormap, str] = "viridis",\n    orientation: Literal["vertical", "horizontal"] = "vertical",\n    layout_reingold_tilford: bool = None,\n    min_cluster_number: Literal[0, 1] = 1,\n    border_size: float = 0.05,\n    figsize: tuple[float, float] = None,\n    arrows: bool = None,\n    node_size: float = 300,\n    node_size_edge: Optional[float] = None,\n    dpi: float = 500,\n    kk: Optional[int] = None,\n) -> DiGraph:\n    """\n\n```\n\n* `data` : Path of csv or DataFrame object.\n* `prefix` : String indicating columns containing clustering information.\n* `images` : Path of directory that contains images.\n* `output_path` : Absolute path to save clustree drawing at. If file extension is supplied, must be .png. If None, then output not written to file.\n* `draw` : Whether to draw the clustree. Defaults to True. If False and output_path supplied, will be overridden.\n* `node_color` : For continuous colormap, use \'samples\' or the name of a metadata column to color nodes by. For discrete colors, use \'prefix\' to color by resolution or specify a fixed color (see Specifying colors in Matplotlib tutorial here: https://matplotlib.org/stable/tutorials/colors/colors.html). If None, default set equal to value of prefix to color by resolution.\n* `node_color_aggr` : If node_color is a column name then a function or string giving the name of a function to aggregate that column for samples in each cluster.\n* `node_cmap` : If node_color is \'samples\' or a column name then a colourmap to use (see Colormap Matplotlib tutorial here: https://matplotlib.org/stable/tutorials/colors/colormaps.html).\n* `edge_color` : For continuous colormap, use \'samples\'. For discrete colors, use \'prefix\' to color by resolution or specify a fixed color (see Specifying colors in Matplotlib tutorial here: https://matplotlib.org/stable/tutorials/colors/colors.html). If None, default set to \'samples\'.\n* `edge_cmap` : If edge_color is \'samples\' then a colourmap to use (see Colormap Matplotlib tutorial here: https://matplotlib.org/stable/tutorials/colors/colormaps.html).\n* `orientation` : Orientation of clustree drawing. Defaults to \'vertical\'.\n* `layout_reingold_tilford` : Whether to use the Reingold-Tilford algorithm for node positioning. Defaults to True if (kk <= 12), False otherwise. Setting True not recommended if (kk > 12) due to memory bottleneck in igraph dependency.\n* `min_cluster_number` : 0 if cluster number is (0, ..., K-1) or 1 if (1, ..., K). Defaults to 1.\n* `border_size` : Border width as proportion of image width. Defaults to 0.05.\n* `figsize` : Parsed to matplotlib to determine figure size. Defaults to (kk/2, kk/2), clipped to a minimum of (3,3) and maximum of (10,10).\n* `arrows` : Whether to add arrows to graph edges. Removing arrows alleviates appearance issue caused by arrows overlapping nodes. Defaults to True.\n* `node_size` : Size of nodes in clustree graph drawing. Parsed directly to networkx.draw_networkx_nodes. Default to 300.\n* `node_size_edge`: Controls edge start and end point. Parsed directly to networkx.draw_networkx_edges.\n* `dpi` : Controls resolution of output if saved to file.\n* `kk` : Choose custom depth of clustree graph.\n\n## Glossary\n\n* *cluster resolution*: Upper case `K`. For example, at cluster resolution `K=2` data is clustered into 2 distinct clusters.\n* *cluster number*: Lower case `k`. For example, at cluster resolution 2 data is clustered into 2 distinct clusters `k=1` and `k=2`.\n* *kk*: highest value of `K` (cluster resolution) shown in clustree.\n* *cluster membership*: The association between data points and cluster numbers for fixed cluster resolution. For example, `[1, 1, 2, 2, 2]` would mean the first 2 data points belong to cluster number `1` and the following 3 data points belong to cluster number `2`.',
    'author': 'Ben Barlow',
    'author_email': 'ben-j-barlow.1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ben-j-barlow/clustree',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
