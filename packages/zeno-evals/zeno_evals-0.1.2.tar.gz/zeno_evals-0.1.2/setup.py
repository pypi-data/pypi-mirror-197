# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeno_evals']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.5.0,<0.6.0', 'pandas>=1.5.3,<2.0.0', 'zenoml>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['zeno-evals = zeno_evals.main:cli']}

setup_kwargs = {
    'name': 'zeno-evals',
    'version': '0.1.2',
    'description': 'Visualize OpenAI evals with Zeno',
    'long_description': '# Zeno 🤝 OpenAI Evals\n\nUse [Zeno](https://github.com/zeno-ml/zeno) to visualize the results of [OpenAI Evals](https://github.com/openai/evals/blob/main/docs/eval-templates.md).\n\n### Usage\n\n```bash\npip install zeno-evals\n```\n\nRun an evaluation following the [evals instructions](https://github.com/openai/evals/blob/main/docs/run-evals.md). This will produce a cache file in `/tmp/evallogs/`.\n\nPass this file to the `zeno-evals` command:\n\n```bash\nzeno-evals /tmp/evallogs/my_eval_cache.jsonl\n```\n\n### Example\n\nWe include an example looking at the [MedMCQA](https://github.com/openai/evals/pull/141) dataset (Thanks to @SinanAkkoyun):\n\n```bash\nzeno-evals ./example_medicine/example.jsonl --functions_file=./example_medicine/distill.py\n```\n\n### Todo\n\n- [ ] Support model-graded evaluations\n- [ ] Support custom evaluation templates (e.g. BLEU for translation)\n',
    'author': 'Alex Cabrera',
    'author_email': 'alex.cabrera@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<=3.11',
}


setup(**setup_kwargs)
