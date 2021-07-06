from setuptools import setup

setup(
    name='Windea Tool', #TESPy, oemof-B3
    version='0.0.0',
    license='MIT',
    description='An example of a python package from pre-existing code',
    long_description=open('README.md').read(),
    url="https://github.com/juliusmeier/windea_tool",

    include_package_data=True,          # https://kiwidamien.github.io/making-a-python-package-vi-including-data-files.html
    package_data={'': ['data/*.xlsx']}, # https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/

    # Needed to actually package something
    packages=['windea_tool'],  # directory containing __init__.py
    # Needed for dependencies
    install_requires=['pandas', 'numpy', 'matplotlib', 'openpyxl', 'xlsxwriter'],

    author='Julius Meier',
)
