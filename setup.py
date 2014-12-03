from setuptools import setup

setup(
    name='excel2xx',
    version='1.0.0',
    packages=['excel2xx'],
    url='https://cupen.github.com',
    license='WTFPL',
    author='cupen',
    install_requires = [
        'xlrd >= 0.9',
        'docopt >= 0.6.0'
    ],
    author_email='cupen@foxmail.com',
    description='Export from excel to something(e.g. json sql lua).',
    # entry_points={
    #     'console_scripts': [
    #         'excel2mysql = excel2mysql:main',
    #         'excel2lua = excel2lua:main'
    #     ]
    # },
    scripts=['excel2json.py']
)
