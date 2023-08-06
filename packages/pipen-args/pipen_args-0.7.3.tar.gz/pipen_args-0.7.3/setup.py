# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_args']

package_data = \
{'': ['*']}

install_requires = \
['pipen-annotate>=0.5,<0.6']

setup_kwargs = {
    'name': 'pipen-args',
    'version': '0.7.3',
    'description': 'Command-line argument parser for pipen.',
    'long_description': '# pipen-args\n\nCommand line argument parser for [pipen][1]\n\n## Usage\n\n```python\nfrom pipen import Proc, Pipen\n# Note that unlike other plugins, you need to import install\n# to activate the plugin\nfrom pipen_args import install  # noqa: F401\n\nclass Process(Proc):\n    """My process\n\n    Input:\n        a: Input data\n    """\n    input = \'a\'\n    input_data = range(10)\n    script = \'echo {{in.a}}\'\n\nPipen().set_start(Process).run()\n```\n\n```shell\n$ python example.py --help\nUsage: test.py [-h | -h+] [options]\n\nUndescribed process.\nUse `@configfile` to load default values for the options.\n\nPipeline Options:\n  --name NAME           The name for the pipeline, will affect the default workdir and\n                        outdir. [default: pipen-0]\n  --profile PROFILE     The default profile from the configuration to run the pipeline.\n                        This profile will be used unless a profile is specified in the\n                        process or in the .run method of pipen. You can check the\n                        available profiles by running `pipen profile`\n  --outdir OUTDIR       The output directory of the pipeline [default: ./<name>_results]\n  --forks FORKS         How many jobs to run simultaneously by the scheduler\n  --scheduler SCHEDULER\n                        The scheduler to run the jobs\n\nNamespace <in>:\n  --in.a A [A ...]      Input data\n\nOptional Arguments:\n  -h, --help, -h+, --help+\n                        show help message (with + to show more options) and exit\n```\n\nSee more examples in `tests/pipelines/` folder.\n\n[1]: https://github.com/pwwang/pipen\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pwwang/pipen-args',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
