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
        'msgpack-python >= 0.4.8'
    ],
    author_email='cupen@foxmail.com',
    description='Export something(e.g. json, msgpack, sql, lua) from Excel to file.',
    entry_points={
       "console_scripts": [
           "excel2xx=excel2xx.main:main_docopt",
       ],
    },
    python_requires='>=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',

)
