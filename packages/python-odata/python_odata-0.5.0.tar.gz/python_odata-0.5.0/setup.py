# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odata', 'odata.tests', 'odata.tests.generated']

package_data = \
{'': ['*'], 'odata': ['reflect-templates/*']}

install_requires = \
['mako>=1.2.4,<2.0.0',
 'python-dateutil>=2.8.2',
 'requests>=2.28.2',
 'rich>=13.3.1']

setup_kwargs = {
    'name': 'python-odata',
    'version': '0.5.0',
    'description': 'A simple library for read/write access to OData services.',
    'long_description': "# python-odata\n\nA simple library for read/write access to OData services.\n\n- Supports OData version 4.0\n- Requires JSON format support from the service\n- Should work on both Python 2.x and 3.x\n\n## Documentation\n\nAvailable on [readthedocs.org](https://python-odata.readthedocs.io/en/latest/index.html)\n\n## Dependencies\n\n- requests >= 2.0\n- python-dateutil\n- rich >= 13.3.1\n\n## Demo\n\nReading data from the Northwind service.\n\n```python\nfrom odata import ODataService\nurl = 'http://services.odata.org/V4/Northwind/Northwind.svc/'\nService = ODataService(url, reflect_entities=True)\nSupplier = Service.entities['Supplier']\n\nquery = Service.query(Supplier)\nquery = query.limit(2)\nquery = query.order_by(Supplier.CompanyName.asc())\n\nfor supplier in query:\n    print('Company:', supplier.CompanyName)\n\n    for product in supplier.Products:\n        print('- Product:', product.ProductName)\n```\n\nWriting changes. Note that the real Northwind service is _read-only_\nand the data modifications do not work against it.\n\n```python\nimport datetime\n\nOrder = Service.entities['Order']\nEmployee = Service.entities['Employee']\n\nempl = Service.query(Employee).first()\n\nquery = Service.query(Order)\nquery = query.filter(Order.ShipCity == 'Berlin')\n\nfor order in query:\n    order.ShippedDate = datetime.datetime.utcnow() \n    order.Employee = empl\n    Service.save(order)\n```\n",
    'author': 'Tuomas Mursu',
    'author_email': 'tuomas.mursu@kapsi.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
