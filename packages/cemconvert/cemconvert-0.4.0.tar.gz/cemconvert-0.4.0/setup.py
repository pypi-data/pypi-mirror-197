from setuptools import setup, find_packages
setup(
    name="cemconvert",
    version="0.4.0",
    packages=find_packages(),
    scripts = ['bin/cemconvert','bin/get_camd_cems'],
    python_requires='>3.6',
    setup_requires=['numpy>=1.19.5','pandas>=1.1.0'],
    package_data={'cemconvert': ['data/*.csv']},
    author_email='beidler.james@epa.gov'
)
