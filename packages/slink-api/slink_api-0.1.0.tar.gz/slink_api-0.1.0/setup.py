# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slink']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.6,<2.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'slink-api',
    'version': '0.1.0',
    'description': 'Simple and expressive REST clients without the fuss',
    'long_description': '# Slink\nInspired by [uplink](https://uplink.readthedocs.io/en/stable/), a simple way to build rest API clients without OpenAPI,\nand without a lot of requests boilerplate.\n\n# Install\n```\npoetry install\n```\n\n# Basic Usage\nModel your resource in Pydantic\n```python\nfrom pydantic import BaseModel\nclass MyResource(BaseModel):\n    name: str\n    value: int\n```\n\nCreate an API\n```python\nfrom slink import Api, get, post, Query, Body\n\nclass MyTestApi(Api):\n\n    # Define a get\n    @get("rest/api/3/{resource_key}")\n    def get_resource(self, resource_key: str):\n        return MyResource(**self.response.json())\n\n    # Define it with some query params\n    @get("rest/api/3/{resource_key}/param", testvalue=Query())\n    def get_resource_with_param(self, resource_key: str, testvalue: str):\n        return MyResource(**self.response.json())\n\n    # And post your body content\n    @post("rest/api/3/{resource_key}", body=Body())\n    def post_resource(self, resource_key: str, body: dict):\n        return MyResource(**self.response.json())\n```\n\nThen use it:\n```python\napi = MyTestApi(base_url="http://example.com/")\nresult = api.get_resource(resource_key="REST")\nresult = api.get_resource_with_param(resource_key="REST", testvalue="test")\nresult = api.post_resource(resource_key="TEST", body={"foo": "bar"})\n```\n\n# Pagination\nSlink allows you to elegantly iterate most style of paged APIs. As example, we can implement one of the most common\npagination patterns, an an offseted pagination API. With such an API, you request an offset of the dataset with some\nlimit on the size of the data returned:\n\n```python\nclass OffsettedPager:\n    def __init__(self, results_per_page=5) -> None:\n        self.results_per_page = results_per_page\n        self.startAt = 0\n        self.total = None  # needs to be determined\n\n    def pages(self, url):\n        while self.total is None or self.startAt < self.total:\n            # yield a tuple of the next url and any parameters to be added to the original request\n            yield url, {"startAt": self.startAt, "results_per_page": self.maxCount}\n            self.startAt += self.results_per_page\n\n    def process(self, response):\n        # update the Pager with any response variables; usually either info about the next page or the total number of pages\n        self.total = response.json()["total"]\n```\n\nYou can then use the pager with the `@get_pages` decorator to iterate through the pages:\n\n```python\nclass PagedApi(Api):\n    @get_pages("rest/api/3/pages", pager=OffsetedPager())\n    def get_paginated(self)\n        # our data field in the json result just contains a list of ints, but they could be a much more complicated object\n        for value in self.response.json()["data"]:\n            yield int(value)\n\napi = PagedApi(base_url=base_url)\nall_results = [e for e in api.get_paginated()]\n```\n\nAnother example would be a pagination API where there is a next link:\n\n```python\nclass LinkedPager:\n    def __init__(self) -> None:\n        self.next_url = None\n\n    def pages(self, url):\n        yield url, {}  # first page is just the raw url\n        while self.next_url:\n            yield self.next_url, {}\n\n    def process(self, response):\n        self.next_url = response.json()["links"].get("next")\n```\n\nNote in both cases, iteration can be stopped early by simply stopping calling the endpoint, ie the following will make\nany more requests once it finds the required value:\n\n```python\nfor e in api.get_paginated():\n    if e == value_to_find:\n        break\n```\n\n# Limitations and TODOs\n- [ ] error handling and robustness\n- [ ] retry patterns\n- [ ] put, patch, del\n- [ ] supporting other http client libraries, including async ones',
    'author': 'James Lloyd',
    'author_email': 'james.allan.lloyd@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
