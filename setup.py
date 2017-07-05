from setuptools import setup

setup (
    name = 'rpq',
    version = '1.0.4',
    description = 'Simple Redis work queue with added features (priorities, pop multiple items at once)',
    long_description = 'README.md',
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
