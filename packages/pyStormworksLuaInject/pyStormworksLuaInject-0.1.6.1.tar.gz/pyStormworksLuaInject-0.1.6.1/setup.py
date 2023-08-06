from setuptools import setup, find_packages

# This call to setup() does all the work
setup(
    name="pyStormworksLuaInject",
    version="0.1.6.1",
    packages=find_packages(),
    install_requires=[
        'vdf;platform_system=="Linux"'
    ]
)