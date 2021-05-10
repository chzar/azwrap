from setuptools import setup, find_packages
setup(
    name='azwrap',
    version='0.3',
    package_dir = {'': 'src'},
    packages = find_packages(where='src'),
    install_requires = ['pyfakefs']
)