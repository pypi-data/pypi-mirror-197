# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_factur_x',
 'pydantic_factur_x.factur_x',
 'pydantic_factur_x.factur_x.code_lists',
 'pydantic_factur_x.order-x']

package_data = \
{'': ['*']}

install_requires = \
['pydantic-xml[lxml]>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'pydantic-factur-x',
    'version': '0.1.0',
    'description': 'Python library for pydantic factur-x bindings',
    'long_description': '# pydantic-factur-x\n\nThe main feature of this Python library is to generate Factur-X and Order-X xml files.\nIt uses pydantic to make more easy, accessible and idiomatic the manipulation of all the elements defined in Factur-X and order-X.\nNo need to hassle with xml, only use pydantic object models.\n\n## What is factur-X ?\n\nFactur-X is a Franco-German standard for hybrid e-invoice (PDF for users and XML data for process automation), the first implementation of the European Semantic Standard EN 16931 published by the European Commission on October 16th 2017. Factur-X is the same standard than ZUGFeRD 2.2.\n\nFactur-X is at the same time a full readable invoice in a PDF A/3 format, containing all information useful for its treatment, especially in case of discrepancy or absence of automatic matching with orders and / or receptions, and a set of invoice data presented in an XML structured file conformant to EN16931 (syntax CII D16B), complete or not, allowing invoice process automation.\n\nThe first objective of Factur-X is to enable suppliers, invoice issuers, to create added-value e-invoices, containing a maximum of information in structured form, according to their ability to produce them in this form, and to let customers recipients free to use the invoice data and / or the readable presentation, depending on their needs and their invoice process maturity on automation.\n\n### order-x\n\nOrder-X is the implementation of Factur-X for purchase orders.\n\n## Installation\n\n(tbd)\n\n## Usage\n\n(tbd)\n\n## License\n\nThis library is published under the MIT licence\n\n\n',
    'author': 'Thomas chiroux',
    'author_email': 'thomas@chiroux.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
