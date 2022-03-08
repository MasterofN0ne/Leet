from setuptools import setup
setup(
    name = 'leet',
    version = '0.1.0',
    packages = ['leet'],
    entry_points = {
        'console_scripts': [
            'leet = leet.__main__:main'
        ]
    })