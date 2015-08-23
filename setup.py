from setuptools import setup

setup(
    name='excel2xx',
    version='0.1.0',
    packages=['excel2xx'],
    url='https://github.com/cupen/excel2xx',
    license='WTFPL',
    author='cupen',
    install_requires=[
        'xlrd >= 0.9',
        'docopt >= 0.6.0',
        'mako >= 1.0.0',
    ],
    author_email='cupen@foxmail.com',
    description='Export excel to something(e.g. json sql lua).',
    scripts=['excel2xx.py']
)
