# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcpts', 'gcpts.sql']

package_data = \
{'': ['*']}

install_requires = \
['db-dtypes>=1.0.5,<2.0.0',
 'gcsfs>=2022.11.0,<2023.0.0',
 'google-cloud-bigquery>=3.4.1,<4.0.0',
 'pandas-gbq>=0.19.1,<0.20.0',
 'pandas>=1.5.2,<2.0.0',
 'pyarrow>=10.0.1,<11.0.0']

setup_kwargs = {
    'name': 'gcpts',
    'version': '0.1.2',
    'description': '',
    'long_description': '# GCP time series\n\n[![codecov](https://codecov.io/gh/richwomanbtc/gcpts/branch/main/graph/badge.svg?token=J728V34ZR5)](https://codecov.io/gh/richwomanbtc/gcpts)\n\n## Requirements\n- Python 3.10+\n\n## Installation\n```\npip install gcpts\n```\n\n## Test\n```\npoetry run pytest -s -vv\n```\n\n## Usage\n\n```python\nimport gcpts\nimport pandas as pd\nimport numpy as np\n\n\n\ngcpts_client = gcpts.GCPTS(\n    project_id="example_project", \n    dataset_id="example_dataset"\n)\n\n# Prepare example data, your data need to have 3 columns named symbol, dt, partition_dt\ndf = pd.DataFrame(np.random.randn(5000, 4))\n\ndf.columns = [\'open\', \'high\', \'low\', \'close\']\n\n# symbol represent a group of data for given data columns\ndf[\'symbol\'] = \'BTCUSDT\'\n\n# timestamp should be UTC timezone but without tz info\ndf[\'dt\'] = pd.date_range(\'2022-01-01\', \'2022-05-01\', freq=\'15Min\')[:5000]\n\n# partition_dt must be date, data will be updated partition by partition with use of this column.\n# Every time, you have to upload all the data for a given partition_dt, otherwise older will be gone.\ndf[\'partition_dt\'] = df[\'dt\'].dt.date.map(lambda x: x.replace(day=1))\n\ngcpts_client.upload(table_name=\'example_table\', df=df)\n```\n\n```python\n# Query for raw data.\nraw_clsoe = gcpts_client.query(\n    table_name=\'example_table\',\n    field=\'close\',\n    start_dt=\'2022-02-01 00:00:00\', # yyyy-mm-dd HH:MM:SS, inclusive\n    end_dt=\'2022-02-05 23:59:59\', # yyyy-mm-dd HH:MM:SS, inclusive\n    symbols=[\'BTCUSDT\'],\n)\n\n# Query for raw data with resampling\nresampeld_daily_close = gcpts_client.resample_query(\n    table_name=\'example_table\',\n    field=\'close\',\n    start_dt=\'2022-01-01 00:00:00\', # yyyy-mm-dd HH:MM:SS, inclusive\n    end_dt=\'2022-01-31 23:59:59\', # yyyy-mm-dd HH:MM:SS, inclusive\n    symbols=[\'BTCUSDT\'],\n    interval=\'day\', # month | week | day | hour | {1,2,3,4,6,8,12}hour | minute | {5,15,30}minute\n    op=\'last\', # last | first | min | max | sum\n)\n```\n\n## Disclaimer\nThis allows you to have SQL injection. Please use it for your own purpose only and do not allow putting arbitrary requests to this library.',
    'author': 'richwomanbtc',
    'author_email': 'richwomanbtc@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
