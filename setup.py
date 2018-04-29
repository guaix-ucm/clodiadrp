
from setuptools import find_packages
from setuptools import setup


setup(
    name='clodiadrp',
    version='1.0.dev0',
    author='Sergio Pascual',
    author_email='sergiopr@fis.ucm.es',
    url='https://github.com/guaix-ucm/numina',
    license='MIT',
    description='CLODIA, example Data Reduction Pipeline for Numina',
    packages=find_packages(),
    package_data={
        'clodiadrp': [
            'drp.yaml',
        ],
        'clodiadrp.instrument.configs': ['*.json']
    },
    install_requires=[
        'numina >= 0.16',
    ],
    entry_points={
        'numina.pipeline.1': [
            'CLODIA = clodiadrp.loader:drp_load',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        'Development Status :: 3 - Alpha',
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Astronomy",
        ],
    long_description=open('README.md').read()
)
