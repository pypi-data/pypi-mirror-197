from setuptools import setup, find_packages

setup(
    name='podaac',
    version='0.1.3',
    description='Shorten the distance between data and human.',
    author='PO.DAAC',
    author_email='podaac@podaac.jpl.nasa.gov',
    url='https://github.com/podaac/podaacpy',
    packages=['podaac'],
    install_requires=[
        'numpy',
        'scipy',
        'xarray',
        'pyresample',
        'matplotlib',
        'cartopy',
        'pandas',
        'h5py',
        'netcdf4',
        'dask',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

