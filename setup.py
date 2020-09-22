from setuptools import setup

setup(
    name='excel2xx',
    version="0.4.0",
    packages=['excel2xx'],
    url='https://github.com/cupen/excel2xx',
    license='WTFPL',
    author='cupen',
    install_requires=[
        'xlrd >= 1.1.0',
        'docopt >= 0.6.0',
        'mako >= 1.0.0',
        'msgpack-python >= 0.4.8'
    ],
    author_email="xcupen@gmail.com",
    description='Export something(e.g. json, msgpack, sql, lua) from Excel to file.',
    entry_points={
       "console_scripts": [
           "excel2xx=excel2xx.main:main_docopt",
       ],
    },
    python_requires='>=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
)
