from setuptools import setup, find_packages

setup(
    name            ='rx_tools',
    version         ='0.0.2',
    description     ='Project containing tools for RX measurement',
    long_description='',
    pymodules       = ['ds_getter'],
    package_dir     = {'' : 'src'},
    install_requires= open('requirements.txt').read().splitlines()
)

