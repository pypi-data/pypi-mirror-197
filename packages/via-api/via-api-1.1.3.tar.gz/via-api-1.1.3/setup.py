from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'cached_property',
    'packaging',
    'reverse_geocoder',
    'fast_json',
    'boto3',
    'haversine',
    'osmnx',
    'scikit-learn',
    'requests',
    'geopandas',
    'python-logging-loki',
    'rtree'
)

setup(
    name='via-api',
    version='1.1.3',
    python_requires='>=3.6',
    description='Analysing and serving crowdsourced road quality data',
    long_description='Analysing and serving crowdsourced road quality data',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/via',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'pull_journeys = via.bin.pull_journeys:main',
            'generate_geojson = via.bin.generate_geojson:main'
        ]
    }
)
