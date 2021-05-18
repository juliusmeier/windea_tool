from setuptools import setup

setup(
    name='Windea Tool', #TESPy, oemof-B3
    version='0.0.0',
    license='MIT',
    description='An example of a python package from pre-existing code',
    long_description=open('README.md').read(),

    # Needed to actually package something
    packages=['windea_tool'],  # directory containing __init__.py
    # Needed for dependencies
    install_requires=['pandas'],

    author='Julius Meier',
)
