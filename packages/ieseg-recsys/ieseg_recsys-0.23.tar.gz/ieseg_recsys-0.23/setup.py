from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ieseg_recsys',
    version='0.23',
    license='MIT',
    author="Philipp Borchert",
    author_email='p.borchert@ieseg.fr',
    packages=find_packages(),
    description = 'Recommendation Systems - IESEG School of Management',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pnborchert',
    keywords='Recommender Systems IESEG',
    install_requires=[
          'scikit-learn',
          'scikit-surprise',
          'pandas',
          'numpy',
      ],

)