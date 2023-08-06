# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apple_news_to_sqlite']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=8.1.3,<9.0.0',
 'requests>=2.28.2,<3.0.0',
 'sqlite-utils>=3.30,<4.0']

entry_points = \
{'console_scripts': ['apple-news-to-sqlite = '
                     'apple_news_to_sqlite.__main__:cli']}

setup_kwargs = {
    'name': 'apple-news-to-sqlite',
    'version': '0.5.2',
    'description': 'Export "Saved Stories" from Apple News to SQLite',
    'long_description': '# apple-news-to-sqlite\n\nExport Apple News Saved Stories to SQLite\n\n## Install\n\n    pip install apple-news-to-sqlite\n\n## Source code\n\n[apple-news-to-sqlite](https://github.com/RhetTbull/apple-news-to-sqlite)\n\n## Usage\n\n    apple-news-to-sqlite articles.db\n    \n    apple-news-to-sqlite --dump\n\nYour Terminal app will require full disk access in order to access the saved article database in the Apple News app sandbox.\n\n## CLI help\n\n<!-- [[[cog\nimport cog\nfrom apple_news_to_sqlite.cli import cli\nfrom click.testing import CliRunner\nrunner = CliRunner()\nresult = runner.invoke(cli, ["--help"])\nhelp = result.output.replace("Usage: cli", "Usage: apple-news-to-sqlite")\ncog.out(\n    "```\\n{}\\n```".format(help)\n)\n]]] -->\n```\nUsage: apple-news-to-sqlite [OPTIONS] [DB_PATH]\n\n  Export your Apple News saved stories/articles to a SQLite database\n\n  Example usage:\n\n      apple-news-to-sqlite articles.db\n\n  This will populate articles.db with an "articles" table containing information\n  about your saved articles.\n\n  Notes:\n\n  The contents of the articles themselves are not stored in the database, only\n  metadata about the article such as title, author, url, etc.\n\n  The date the article was saved is in GMT.\n\nOptions:\n  --version       Show the version and exit.\n  --dump, --json  Print saved stories to standard output as JSON.\n  --all           Process all saved articles; if not specified, only saved\n                  articles that have not previously been stored in the database\n                  are processed.\n  --schema        Create database schema and exit.\n  --help          Show this message and exit.\n\n```\n<!-- [[[end]]] -->\n\n## Using apple-news-to-sqlite in your own Python code\n\n`get_saved_articles()` returns a list of dictionaries, each representing a saved article with the\nfollowing keys:\n\n    * id: str\n    * date: datetime.datetime\n    * url: str\n    * title: str\n    * description: str\n    * image: str\n    * author: str\n\n```pycon\n>>> from apple_news_to_sqlite import get_saved_articles\n>>> articles = get_saved_articles()\n```\n\n## How it works\n\nThrough reverse engineering, it was determined that the Apple News app stores\nsaved articles in a file called `reading-list` in the following directory:\n\n`~/Library/Containers/com.apple.news/Data/Library/Application Support/com.apple.news/com.apple.news.public-com.apple.news.private-production/`\n\nThis format of this file is unknown but it is a binary file that contains two embedded \n[binary plist](https://medium.com/@karaiskc/understanding-apples-binary-property-list-format-281e6da00dbd)\nfiles. The first contains an [NSKeyedArchiver](https://developer.apple.com/documentation/foundation/nskeyedarchiver)\nobject which I have not yet inspected. The second bplist contains a list of saved article IDs along with the date\nthey were saved. The article IDs are used to look up the article data on Apple\'s News site and the article data\nis extracted with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).\n\n## Testing\n\nThe code is at the "it works on my machine" stage of testing. (M1 Mini, macOS Ventura 13.1)\n\nI\'ve also tested this on macOS Catalina 10.15.7 and it appears to work correctly.\n\nIf it doesn\'t work for you, please open an issue!\n\n## Contributing\n\nContributions of all types are welcome! Fork the repo, make a branch, and submit a PR.\n\nSee [README_DEV.md](README_DEV.md) for developer notes.\n\n## Thanks\n\nThanks to [Simon Willison](https://simonwillison.net/) who inspired this project\nwith his excellent "everything-to-sqlite" [dogsheep](https://github.com/dogsheep) project.\n\nThanks Simon also for the excellent tools\n[sqlite-utils](https://github.com/simonw/sqlite-utils) and [Datasette](https://datasette.io).\n\nThanks also to [Dave Bullock](https://github.com/eecue) who inspired this project and helped\ntremendously with the reverse engineering and initial code.\n\n## License\n\nMIT License\n',
    'author': 'Rhet Turnbull',
    'author_email': 'rturnbull+git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/RhetTbull/apple-news-to-sqlite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
