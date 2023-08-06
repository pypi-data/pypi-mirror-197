# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cluster_colors']

package_data = \
{'': ['*']}

install_requires = \
['colormath>=3.0.0,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'paragraphs>=0.2.0,<0.3.0',
 'pymonad>=2.4.0,<3.0.0',
 'stacked-quantile>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'cluster-colors',
    'version': '0.6.0',
    'description': 'Cluster color vectors with kmedians',
    'long_description': 'Divisive (but not hierarchical) clustering.\n\nSlow, but clustering exactly how I wanted it. Iteratively split cluster with highest SSE. Splits are used to find new exemplars, which are thrown into k-medians with existing exemplars.\n\nAdvantages:\n* finds big clusters\n* deterministic\n* robust to outliers\n* fast for what it is, can easily split a few thousand members into a small number of clusters\n* decisions made early on do not effect the result as much as they would in true hierarchical clustering\n* has strategies to avoid ties or arbitrary (even if deterministic) decisions with small member sets\n\nDisadvantages:\n* child clusters will not necessarily contain (or only contain) the members of the parent, so this is not hierarchical (unlike agglomerative clustering where you can build a tree and then transverse it cheaply)\n* as a result of not being hierarchical, it is not straightforward to undo changes if you end up with, for instance, two near-identical exemplars. I have implemented "undo" for the specific method `split_to_se`, but I have not implemented a general "undo" method. Tie-breaking strategies will always use merge instead of undo anyway, so it\'s important to expect that one list of members might end up in n-clusters multiple ways.\n* slows down as the number of clusters grows, not the best way to de-cluster all the way back to constituent members\n* uses Euclidean distance (sum squared error) for many steps. Delta e is used for final splitting criteria.\n\nThis clustering is designed for questions like "what are the two dominant colors in this image (respecting transparency)?"\n\nOnce you split a cluster, it\'s acceptable to just throw it away. And you will probably only need the exemplars of the clusters you do keep, though you could re-cluster each cluster\'s members for a semi-hierarchical clustering scheme.\n\n## Three large steps in the background\n\n### Average colors by n-bit representation\n\n`pool_colors`: reduce 8-bit image colors (potentially 16_777_216 colors) to a maximum of 262_144 by averaging. The ouput of `pool_colors` will also contain a weight axis for each color, representing the combined opacity of all pixels of that color.\n\n### Median cut along longest axis\n\n`cut_colors`: reduce colors to around 512 by recursively splitting along longest axis (longest actual axis. Not constrained to x, y, or, z axes).\n\n### k-medians clustering\n\n`KMediansClusters`: split and merge clusters. Again this is *not* hierarchical, so the sequence\n\n* start\n* split\n* merge\n\nis not guaranteed to bring you back to start. The merge methods are "public", but their principal use is to break ties in order to maintain deterministic results. For example:\n\n* start with one cluster with 100 members\n* split this cluster recursively into five clusters (30, 30, 20, 10, 10)\n* ask for the largest cluster, and there\'s a tie\n* KMediansClusters will recursively merge the closest two clusters until the tie is broken\n\n\n##\n\n    pip install cluster_colors\n\n## Basic usage\n\n~~~python\nfrom cluster_colors import get_image_clusters\n\nclusters = get_image_clusters(image_filename) # one cluster at this point\nclusters.split_to_delta_e(16)\nsplit_clusters = clusters.get_rsorted_clusters()\n\ncolors: list[tuple[float, float, float]] = [c.exemplar for c in split_clusters]\n\n# to save the cluster exemplars as an image file\n\nshow_clusters(split_clusters, "open_file_to_see_clusters")\n~~~\n',
    'author': 'Shay Hill',
    'author_email': 'shay_public@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
