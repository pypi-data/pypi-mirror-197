# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdk_proxy_api_client',
 'cdk_proxy_api_client.admin_auth',
 'cdk_proxy_api_client.common',
 'cdk_proxy_api_client.models',
 'cdk_proxy_api_client.specs',
 'cdk_proxy_api_client.tenant_mappings',
 'cdk_proxy_api_client.tools']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

extras_require = \
{'cli': ['jsonschema>=4.17.3,<5.0.0',
         'compose-x-common>=1.2.8,<2.0.0',
         'importlib-resources>=5.12.0,<6.0.0'],
 'tools': ['jsonschema>=4.17.3,<5.0.0',
           'compose-x-common>=1.2.8,<2.0.0',
           'importlib-resources>=5.12.0,<6.0.0']}

entry_points = \
{'console_scripts': ['cdk-cli-create-tenant-token = '
                     'cdk_proxy_api_client.tools.create_tenant_token:main',
                     'cdk-cli-import-tenant-mappings = '
                     'cdk_proxy_api_client.tools.tenant_mappings_manager:main']}

setup_kwargs = {
    'name': 'cdk-proxy-api-client',
    'version': '0.1.2',
    'description': 'Conduktor Proxy API Client',
    'long_description': '# cdk-proxy-api-client\n\nAPI Client library to interact with Conduktor Proxy\n\nCurrent version: v1beta1\n\n\n## Getting started\n\nFirst, create a Proxy Client\n\n```python\nfrom cdk_proxy_api_client.proxy_api import ApiClient, ProxyClient\n\napi = ApiClient("localhost", port=8888, username="superUser", password="superUser")\nproxy_client = ProxyClient(api)\n```\n\n### Features\n\nNote: we assume you are re-using the ``proxy_client`` as shown above.\n\n* Create new Token for a tenant\n\n```python\nfrom cdk_proxy_api_client.admin_auth import AdminAuth\n\nadmin = AdminAuth(proxy_client)\nadmin.create_tenant_credentials("a_tenant_name")\n```\n\n* List all topic mappings for a tenant\n\n```python\nfrom cdk_proxy_api_client.proxy_api import Multitenancy\n\ntenants_mgmt = Multitenancy(proxy_client)\ntenants = tenants_mgmt.list_tenants(as_list=True)\n```\n\n* Create a new mapping for a tenant\n* Delete a tenant - topic mapping\n* Delete all topic mappings for a tenant\n\n```python\nfrom cdk_proxy_api_client.tenant_mappings import TenantMappings\n\ntenant_mappings_mgmt = TenantMappings(proxy_client)\ntenant_mappings_mgmt.create_tenant_topic_mapping(\n    "tenant_name", "logical_name", "real_name"\n)\ntenant_mappings_mgmt.delete_tenant_topic_mapping("tenant_name", "logical_name")\n```\n\n## Testing\nThe testing is for now very manual. See ``e2e_testing.py``\n\nPytest will be added later on\n\n\n## Tools & CLI\n\nTo simplify the usage of the client, you can use some CLI tools\n\n### cdk-cli-import-tenant-mappings\n\n```shell\nusage: Create tenant mappings from configuration file [-h] -f MAPPINGS_FILE --username USERNAME --password PASSWORD --url URL [--to-yaml]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -f MAPPINGS_FILE, --mappings-file MAPPINGS_FILE\n                        Path to the tenants mappings config file\n  --username USERNAME\n  --password PASSWORD\n  --url URL\n  --to-yaml             Output the mappings in YAML\n```\n\nexample file:\n\n```yaml\n---\n# example.config.yaml\n\ntenant_name: application-01\nignore_duplicates_conflict: true\nmappings:\n  - logicalTopicName: data.stock\n    physicalTopicName: data.stock\n    readOnly: true\n```\n\n```shell\ncdk-cli-import-tenant-mappings -f example.config.yaml \\\n  --username ${PROXY_USERNAME} \\\n  --password ${PROXY_PASSWORD} \\\n  --url ${PROXY_URL}\n```\n\n### cdk-cli-create-tenant-token\n\nCreate a new user tenant token\n\n```shell\ncdk-cli-create-tenant-token \\\n  --username ${PROXY_USERNAME} \\\n  --password ${PROXY_PASSWORD} \\\n  --url ${PROXY_URL} \\\n  --lifetime-in-seconds 3600  \\\n  --tenant-name js-fin-panther-stg\n```\n',
    'author': 'John "Preston" Mille',
    'author_email': 'john@ews-network.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
