from setuptools import setup

setup(
    name='gist-to-do',
    version='1.0',
    py_modules=['gistToDo'],
    include_package_data=True,
    install_requires=[
        'click',
        'PyGithub'
    ],
    entry_points='''
        [console_scripts]
        gistToDo=gistToDo.gistToDo
    ''',
)