# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['basic']
install_requires = \
['pyroll-cli>=2.0,<3.0',
 'pyroll-core>=2.0,<3.0',
 'pyroll-export>=2.0,<3.0',
 'pyroll-freiberg-flow-stress>=2.0,<3.0',
 'pyroll-hensel-power-and-labour>=2.0,<3.0',
 'pyroll-hitchcock-roll-flattening>=2.0,<3.0',
 'pyroll-integral-thermal>=2.0,<3.0',
 'pyroll-lendl-equivalent-method>=2.0,<3.0',
 'pyroll-report>=2.0,<3.0',
 'pyroll-wusatowski-spreading>=2.0,<3.0',
 'pyroll-zouhar-contact>=2.0,<3.0']

setup_kwargs = {
    'name': 'pyroll-basic',
    'version': '2.0',
    'description': 'A meta package for installing quickly the PyRolL core and a set of basic plugins and extensions.',
    'long_description': '# PyRolL Basic Meta Package\n\nThis package does not introduce any new functionality, it works just as a meta-package to simplify the installation of\nthe PyRolL core and a couple of basic plugins through its dependencies.\n\nThe following packages are installed alongside their own dependencies:\n\n- `pyroll`\n- `pyroll-integral-thermal`\n- `pyroll-hensel-power-and-labour`\n- `pyroll-wusatowski-spreading`\n- `pyroll-zouhar-contact`\n- `pyroll-freiberg-flow-stress`\n- `pyroll-hitchcock-roll-flattening`\n\nBy importing this package with `import pyroll.basic`, all listed packages are imported and thus registered as active\nplugins.\nThe public API of this package is the union of all those packages.\nSo with `import pyroll.basic as pr` one has access to all public APIs of those packages under one single alias.',
    'author': 'Max Weiner',
    'author_email': 'max.weiner@imf.tu-freiberg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyroll-project.github.io',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
