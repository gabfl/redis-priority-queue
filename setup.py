from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup (
    name = 'rpq',
    version = '1.1',
    description = 'Simple Redis work queue with added features (priorities, pop multiple items at once)',
    long_description = long_description,
    author = 'Gabriel Bordeaux',
    author_email = 'pypi@gab.lc',
    url = 'https://github.com/gabfl/redis-priority-queue',
    license = 'MIT',
    packages = ['rpq', 'rpq_src'],
    package_dir = { 'rpq': 'clients/python/lib', 'rpq_src': 'src' },
    package_data={
      'rpq_src': ['*.lua'],
   },
    install_requires = ['redis', 'argparse', 'prettytable'], # external dependencies
    entry_points = {
        'console_scripts': [
            'rpq_monitor = rpq_src.queue_monitor:main',
        ],
    },
)
