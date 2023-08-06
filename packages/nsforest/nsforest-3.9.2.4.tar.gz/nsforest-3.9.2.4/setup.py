"""A setuptools based setup module.

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))
setup(
    name='nsforest',  # Required
    version='3.9.2.4',  # Required
    description='NSForest: identifying minimal markers genes for cell types',  # Required
    long_description =  "A machine learning method for the discovery of minimum marker gene combinations for cell type identification from single-cell RNA sequencing",
    long_description_content_type='text/plain',  # Optional (see note above)
    url='https://github.com/JCVenterInstitute/NSForest',  # Optional
    author='Renee Zhang, Richard Scheuermann, Brian Aevermann',  # Optional
    author_email='zhangy@jcvi.org, rscheuermann@jcvi.org, baevermann@chanzuckerberg.com',  # Optional
    classifiers=[ 
    
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Bioinformaticians',
        'Topic :: Machine Learning :: scRNA-seq',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3'
    ],
    packages= find_packages(),  # Required
    install_requires = [
        'python>=3.8',
        'scanpy>=1.9.3',
    ],
)