from setuptools import setup, find_packages

setup(
    name='Matilda',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'my_script=my_package.my_module:main'
        ]
    }
)

