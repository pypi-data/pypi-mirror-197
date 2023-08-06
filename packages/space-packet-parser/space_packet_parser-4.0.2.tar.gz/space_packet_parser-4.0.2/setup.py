# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['space_packet_parser']

package_data = \
{'': ['*']}

install_requires = \
['bitstring>=3.0.0,<5']

setup_kwargs = {
    'name': 'space-packet-parser',
    'version': '4.0.2',
    'description': 'A CCSDS telemetry packet decoding library based on the XTCE packet format description standard.',
    'long_description': '# Space Packet Parser - a configurable parser for CCSDS telemetry packets\nThis is a package for decoding CCSDS telemetry packets according to an XTCE or CSV packet structure definition. \nIt is based on the UML model of the XTCE spec and aims to support all but the most esoteric elements of the \nXTCE telemetry packet specification.\n\nResources:\n- [XTCE (Green Book - Informational Report)](https://public.ccsds.org/Pubs/660x2g2.pdf)\n- [XTCE Element Description (Green Book - Informational Report)](https://public.ccsds.org/Pubs/660x1g2.pdf)\n- [XTCE (Blue Book - Recommended Standard)](https://public.ccsds.org/Pubs/660x0b2.pdf)\n\n## Installation\n```bash\npip install space_packet_parser\n```\n',
    'author': 'Gavin Medley',
    'author_email': 'gavin.medley@lasp.colorado.edu',
    'maintainer': 'Gavin Medley',
    'maintainer_email': 'gavin.medley@lasp.colorado.edu',
    'url': 'https://github.com/medley56/space_packet_parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
