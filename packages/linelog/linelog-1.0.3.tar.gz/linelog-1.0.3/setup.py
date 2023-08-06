# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linelog']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'plotille>=5.0.0,<6.0.0',
 'pygit2>=1.11.1,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=13.3.1,<14.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['linelog = linelog.console:run']}

setup_kwargs = {
    'name': 'linelog',
    'version': '1.0.3',
    'description': 'Track your total lines of code committed in git, and view the trend over time via a simple TUI graph visualization',
    'long_description': "# Linelog\n## Summary\n\n`linelog` is a CLI program that scans your local git repositories generates a summary of your total lines of code committed, broken down by language. For example, if I run `linelog -a` on my main desktop computer, it generates this:\n\n\n![example-day](screenshots/linelog-example-day.png)\n\nThis isn't very exciting since I've not done much today (look, work-life balance is important.)  With the `-d` flag you can look back further in time, and see the results as a nice graph:\n\n\n![example-2week](screenshots/linelog-example-2week.png)\n\n*Hey, wait a second!*, you exclaim, *This very project has more than 651 lines of Python code, and most of it was committed in that very interval!* That's very astute of you, you have a real eagle eye. The discrepency comes from the fact that `linelog` does its best to count *logical* lines of code by skipping comments and whitespaces. You can customize what counts as a line for a given filetype; see the section on [configuration](https://github.com/keagud/linelog#the-config-file)\n\n\n## Installation (Pip)\n`linelog` is on PyPI. Install it with `pip` or `pipx`:\n```\npip install linelog\n```\n\n## Usage and Configuration\n\n`linelog` uses this algorithm to count lines (simplified a bit):\n\n- For the specified repository, iterate *pairwise* through all commits in the specified timeframe that have the specified author. \n- For each pair of sequential commits, apply the pattern matches specified in the config to count the total lines for each file. Then subtract the earlier line count from the later.\n  - If the difference is *negative* (the later commit has fewer net lines), it is instead counted as zero. \n  This is essentially the only part of the counting behavior that the user cannot edit directly, both for technical and philosophical reasons. The point of `linelog` is to get a broad sense of productivity over a timespan, using lines of code written as a proxy. It is *not* meant to work as a diff generator - there are many many tools out there for that!\n- Results for each filetype are collected and then summed for the final result. \n\n### Usage\nA summary of available options is viewable with `linelog --help` \n```\nusage: linelog [-h] [-u USERNAME] [-c] [-r] [-a] [-d DAYS] [start_dir]\n\npositional arguments:\n  start_dir             The directory to scan. Defaults to the current working\n                        directory if unspecified\n\noptions:\n  -h, --help            show this help message and exit\n  -u USERNAME, --username USERNAME\n                        Limit the scan to commits by this username. If\n                        unspecified, the username set in the global git config\n                        file (if present) is used. If no username is given by\n                        either of these methods, or if the -c option is\n                        passed, all commits are considered regardless of\n                        author\n  -c, --all-commits     Consider all commits by any user. Overrides the\n                        --username option if present.\n  -r, --recursive       If no repository is found in the given directory,\n                        search all subdirectories recursively and consider any\n                        repositories found there. If the top level directory\n                        is a repository, this does nothing.\n  -a, --all             Start the scan in the home directory, and search all\n                        subdirectories for repositories. Same as 'linelog ~\n                        -r'\n  -d DAYS, --days DAYS  The number of days in the past to traverse when\n                        scanning a repository for relevant commits. If\n                        unspecified defaults to 1 (only today). The output\n                        graph is only generated if this is greater than one\n```\n\n### The Config File\n`linelog` generates a config file at `~/.config/linelog/config.yaml` when run for the first time. The default config contains what I think are sensible defaults, but if you disagree you're free to change almost all of the line counting behavior. \n\nConfig options take the form of regular expressions; when the program encounters a line that matches one of the expressions for a given filetype, it will not count it. See the comments in `config.yaml` for more details\n\n\n\n\n",
    'author': 'keagud',
    'author_email': 'keagud@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
