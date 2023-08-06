# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zamm',
 'zamm.actions',
 'zamm.actions.edit_file',
 'zamm.actions.follow_tutorial',
 'zamm.actions.note',
 'zamm.actions.use_terminal',
 'zamm.agents',
 'zamm.chains',
 'zamm.chains.general',
 'zamm.chains.general.choice',
 'zamm.chains.general.get_dict',
 'zamm.llms',
 'zamm.prompts',
 'zamm.resources',
 'zamm.resources.tutorials',
 'zamm.resources.tutorials.issues',
 'zamm.resources.tutorials.setup',
 'zamm.resources.tutorials.setup.repo',
 'zamm.resources.tutorials.setup.tools',
 'zamm.tasks']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'langchain-visualizer>=0.0.14,<0.0.15',
 'openai>=0.27.0,<0.28.0',
 'pexpect>=4.8.0,<5.0.0',
 'pyyaml>=6.0,<7.0',
 'simple-term-menu>=1.6.1,<2.0.0',
 'tiktoken>=0.2.0,<0.3.0',
 'typer[all]>=0.7.0,<0.8.0',
 'ulid>=1.1,<2.0',
 'vcr-langchain>=0.0.17,<0.0.18']

entry_points = \
{'console_scripts': ['zamm = zamm.cli:app']}

setup_kwargs = {
    'name': 'zamm',
    'version': '0.0.5',
    'description': 'General automation driver',
    'long_description': '# ZAMM\n\nThis is an informal automation tool where you show GPT how to do something, and have it do it for you afterwards. This is good for boring but straightforward tasks that you haven\'t gotten around to writing a proper script to automate.\n\nWe are entering a time when our target audiences may include machines as well as humans. As such, this tool will generate tutorials that you can edit to make pleasant for both humans and LLMs alike to read.\n\n**This is an experimental tool, and has only been run on WSL Ubuntu so far.** It seems to work ok on the specific examples below. YMMV. Please feel free to add issues or PRs.\n\n## Quickstart\n\n`pipx` recommended over `pip` for install because it should allow you to run this with a different version of `langchain` than the one you might have installed:\n\n```bash\npipx install zamm\n```\n\nTeach GPT to do something:\n\n```bash\nzamm teach\n```\n\nYou will be roleplaying the LLM. The results of your interaction will be output as a Markdown tutorial file, which you can then edit to be more human-readable. See [this example](zamm/resources/tutorials/hello.md) of teaching the LLM how to create a "Hello world" script.\n\nAfterwards, you can tell the LLM to do a slightly different task using that same tutorial:\n\n```bash\nzamm execute --task \'Write a script goodbye.sh that prints out "Goodbye world". Execute it.\' --documentation zamm/resources/tutorials/hello.md\n```\n\nThis results in [this example transcript](demos/hello-transcript.md) of LLM interactions. **Note that GPT successfully generalizes from the tutorial to code in a completely different language based just on the difference in filenames.** Imagine having to manually add that feature to a script!\n\n### Using internal tutorials\n\nSelect any of the [prepackaged tutorials](zamm/resources/tutorials/) as documentation by prefacing their filename with `@internal`. The `.md` extension is optional.\n\nFor example:\n\n```bash\nzamm execute --task \'Protect the `main` branch\' --documentation @internal/branch-protection\n```\n\nto protect the `main` branch of the project in the current directory on Github. (Note that this tutorial was written in mind for ZAMM-built projects, so YMMV for using this on custom projects.)\n\n### Sessions\n\nSessions are recorded in case a crash happens, or if you want to change something up. On Linux, sessions are saved to `~/.local/share/zamm/sessions/`. To continue from the most recent session, run\n\n```bash\nzamm teach --last-session\n```\n\n### Free-styling\n\nYou can also simply tell the LLM to do something without teaching it to do so beforehand. However, this is a lot more brittle. An example of a free-style command that works:\n\n```bash\nzamm execute --task \'Write a script hello.py that prints out "Hello world". Execute it.\'\n```\n\nThe resulting transcript can be found [here](demos/freestyle-hello-transcript.md).\n\n## Prompting\n\nWhen a step is failing and you need faster iteration by repeatedly testing a single prompt, you can do so with the `prompt` command. First, write your prompt out to a file on disk. Then run this command:\n\n```bash\nzamm prompt --stop \'\\n\' --raw <path-to-prompt>\n```\n',
    'author': 'Amos Jun-yeung Ng',
    'author_email': 'me@amos.ng',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
