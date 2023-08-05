# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wordcab', 'wordcab.core_objects']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1', 'requests>=2.28.1', 'validators>=0.20.0']

entry_points = \
{'console_scripts': ['wordcab = wordcab.__main__:main']}

setup_kwargs = {
    'name': 'wordcab',
    'version': '0.6.1',
    'description': 'Wordcab Python SDK',
    'long_description': '<h1 align="center">Wordcab Python</h1>\n\n<div align="center">\n\t<a  href="https://pypi.org/project/wordcab" target="_blank">\n\t\t<img src="https://img.shields.io/pypi/v/wordcab.svg" />\n\t</a>\n\t<a  href="https://pypi.org/project/wordcab" target="_blank">\n\t\t<img src="https://img.shields.io/pypi/pyversions/wordcab" />\n\t</a>\n\t<a  href="https://github.com/Wordcab/wordcab-python/blob/main/LICENSE" target="_blank">\n\t\t<img src="https://img.shields.io/pypi/l/wordcab" />\n\t</a>\n\t<a  href="https://github.com/Wordcab/wordcab-python/actions?workflow=Tests" target="_blank">\n\t\t<img src="https://github.com/Wordcab/wordcab-python/workflows/Tests/badge.svg" />\n\t</a>\n\t<a  href="https://app.codecov.io/gh/Wordcab/wordcab-python" target="_blank">\n\t\t<img src="https://codecov.io/gh/Wordcab/wordcab-python/branch/main/graph/badge.svg" />\n\t</a>\n</div>\n<br>\n<div align="center">\n\t<a href="https://linkedin.com/company/wordcab" target="_blank">\n\t\t<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />\n\t</a>\n</div>\n\n# What is Wordcab?\n\n- **Summarize any business communications at scale with Wordcab\'s API.**\n- **Wordcab** is a summarization service that provides a simple API to summarize any `audio`, `text`, or `JSON` file.\n- It also includes compatibility with famous transcripts platforms like\n  - [![AssemblyAI](https://img.shields.io/badge/AssemblyAI-blue)](https://www.assemblyai.com/)\n  - [![Deepgram](https://img.shields.io/badge/Deepgram-green)](https://deepgram.com/)\n  - [![Rev.ai](https://img.shields.io/badge/Rev.ai-orange)](https://www.rev.ai/)\n  - [![Otter.ai](https://img.shields.io/badge/Otter.ai-purple)](https://otter.ai/)\n  - [![Sonix.ai](https://img.shields.io/badge/Sonix.ai-yellow)](https://sonix.ai/)\n\n# Getting started\n\nYou can learn more about Wordcab services and pricing on our [website](https://wordcab.com/).\n\nIf you want to try out the API, you can [signup](https://wordcab.com/signup/) for a free account and start using the API\nright away.\n\n# Requirements\n\n- OS:\n  - ![Linux](https://img.shields.io/badge/-Linux-orange?style=flat-square&logo=linux&logoColor=white)\n  - ![Mac](https://img.shields.io/badge/-Mac-blue?style=flat-square&logo=apple&logoColor=white)\n  - ![Windows](https://img.shields.io/badge/-Windows-blue?style=flat-square&logo=windows&logoColor=white)\n- Python:\n  - ![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)\n\n# Installation\n\nYou can install _Wordcab Python_ via [pip] from [PyPI]:\n\n```console\n$ pip install wordcab\n```\n\nStart using the API with any python script right away!\n\n# Usage\n\n## Start Summary full pipeline\n\n```python\nimport time\nfrom wordcab import retrieve_job, retrieve_summary, start_summary\nfrom wordcab.core_objects import AudioSource, GenericSource, InMemorySource\n\n\n# Prepare your input source\n## For a transcript stored as a .txt or .json file\nsource = GenericSource(filepath="path/to/file.txt")  # Or file.json\n## For a transcript stored as an audio file\nsource = AudioSource(filepath="path/to/file.mp3")\n## For a transcript already in memory\ntranscript = {"transcript": ["SPEAKER A: Hello.", "SPEAKER B: Hi."]}\nsource = InMemorySource(obj=transcript)\n\n# Launch the Summarization job\njob = start_summary(\n\tsource_object=source,\n\tdisplay_name="sample_txt",\n\tsummary_type="narrative",\n\tsummary_lens=[1, 3],\n\ttags=["sample", "text"],\n)\n\n# Wait for the job completion\nwhile True:\n\tjob = retrieve_job(job_name=job.job_name)\n\tif job.job_status == "SummaryComplete":\n\t\tbreak\n\telse:\n\t\ttime.sleep(3)\n\n# Get the summary id\nsummary_id = job.summary_details["summary_id"]\n# Retrieve the summary\nsummary = retrieve_summary(summary_id=summary_id)\n\n# Get all information from the retrieved summary\nfor k, v in summary.__dict__.items():\n    print(f"{k}: {v}")\n\n# Get the summary as one block of text\nfor k, v in summary.summary.items():\n\tprint(f"Summary Length: {k}")\n\tprint(f"Summary: {v[\'structured_summary\'][0].summary}")\n```\n\n# Documentation\n\nPlease see the [Documentation](https://wordcab-python.readthedocs.io/) for more details.\n\n# Contributing\n\nContributions are very welcome. 🚀\nTo learn more, see the [Contributor Guide].\n\n# License\n\n- Distributed under the terms of the [![Apache 2.0 License Badge](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\n- _Wordcab Python SDK_ is free and open source software.\n\n# Issues\n\nIf you encounter any problems,\nplease [file an issue](https://github.com/Wordcab/wordcab-python/issues) along with a detailed description.\n\n# Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/Wordcab/wordcab-python/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/Wordcab/wordcab-python/blob/main/LICENSE\n[contributor guide]: https://github.com/Wordcab/wordcab-python/blob/main/CONTRIBUTING.md\n[command-line reference]: https://wordcab-python.readthedocs.io/en/latest/usage.html\n',
    'author': 'Wordcab',
    'author_email': 'info@wordcab.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Wordcab/wordcab-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
