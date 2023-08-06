# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['debiantospdx']

package_data = \
{'': ['*']}

install_requires = \
['scancode-toolkit==31.2.4']

entry_points = \
{'console_scripts': ['debiantospdx = debiantospdx.cli:entry']}

setup_kwargs = {
    'name': 'debiantospdx',
    'version': '0.1.13',
    'description': 'This tool generate SPDX files from your Debian system / packages',
    'long_description': '# debiantospdx\n\n[![Apache2.0 License](https://img.shields.io/badge/License-Apatch2.0-green.svg?style=for-the-badge)](https://choosealicense.com/licenses/apache-2.0/)\n\nシステムに存在するすべてのDebianパッケージのSPDXファイルを生成するコマンドラインツール\n\nパッケージ名・バージョン・ソフトウェアライセンス・コピーライト・パッケージ間の依存関係の解析を行う\n\n## Usage/Examples\n\n```bash\ndebiantospdx [ディレクトリのパス] [オプション]\n```\nSPDXファイルを置くパスをして実行する\n\nオプションとその内容については以下の通り\n\n引数を必要とするものは引数の例を併記する\n```bash\n  -h, --help            HELPメッセージの出力\n  \n  -p, --person          SPDXファイルの作者名（引数: 個人名（ex. TK tanab））\n  -pe                   SPDXファイルの作者のメールアドレス（引数: 個人のメールアドレス（ex. tanab@hoge.com）\n  -o, --organization    SPDXファイルの作者名（引数: 組織名（ex. HIGO Lab））\n  -oe                   SPDXファイルの作者のメールアドレス（引数: 組織のメールアドレス（ex. higo-lab@hoge.com）\n  \n  --package             指定したパッケージのPDXファイルを生成（引数: パッケージ名（ex. python3.10））\n  --all                 インストール済みのすべてのパッケージのSPDXファイルを生成\n  --search              指定したパッケージの情報をSPDXファイルから抽出（引数: パッケージ名（ex. python3.10））\n```\npackage, all, searchはどれか1つのみを選択して実行する．\n\npackageまたはallを選択した場合は作者名となる個人名または組織名のうち少なくとも1つを必要とする\n\n## Authors\n\n- [@tk-tanab](https://github.com/tk-tanab)\n\n\n## License\n\n- [Apatch2.0](https://choosealicense.com/licenses/apache-2.0/)\n\n',
    'author': 'tk-tanab',
    'author_email': 'tk-tanab@ist.osaka-u.ac.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tk-tanab/debiantospdx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
