# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dodo_is_api', 'dodo_is_api.connection', 'dodo_is_api.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0']

setup_kwargs = {
    'name': 'dodo-is-api',
    'version': '0.2.0',
    'description': '',
    'long_description': "# 🍕 Dodo IS API Wrapper\n\n#### 📝 [Changelog](./CHANGELOG.md) is here.\n\n### 🧪 Usage:\n\n```python\nimport datetime\nfrom uuid import UUID\n\nfrom dodo_is_api.connection import DodoISAPIConnection\nfrom dodo_is_api.connection.http_clients import closing_http_client\nfrom dodo_is_api.mappers import map_late_delivery_voucher_dto\n\naccess_token = 'my-token'\ncountry_code = 'kg'\n\nunits = [UUID('e0ce0423-3064-4e04-ad3e-39906643ef14'), UUID('bd09b0a8-147d-46f7-8908-874f5f59c9a2')]\nfrom_date = datetime.datetime(year=2023, month=3, day=16)\nto_date = datetime.datetime(year=2023, month=3, day=17)\n\nwith closing_http_client(access_token=access_token, country_code=country_code) as http_client:\n    dodo_is_api_connection = DodoISAPIConnection(http_client=http_client)\n\n    # it will handle pagination for you\n    for late_delivery_vouchers in dodo_is_api_connection.iter_late_delivery_vouchers(\n            from_date=from_date,\n            to_date=to_date,\n            units=units\n    ):\n        \n        # map to dataclass DTO if you need\n        late_delivery_voucher_dtos = [\n            map_late_delivery_voucher_dto(late_delivery_voucher)\n            for late_delivery_voucher in late_delivery_vouchers\n        ]\n        ...\n```\n",
    'author': 'Eldos',
    'author_email': 'eldos.baktybekov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
