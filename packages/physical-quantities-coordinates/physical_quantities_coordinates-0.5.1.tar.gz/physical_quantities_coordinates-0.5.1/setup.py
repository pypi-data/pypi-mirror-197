from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='physical_quantities_coordinates',
    version='0.5.1',
    packages=['physical_quantities_coordinates'],
    url='https://gitlab.com/frankmobley/physical_quantities_coordinates',
    license='',
    author='Dr. Frank Mobley',
    author_email='frank.mobley.1@afrl.af.mil',
    description='A collection of classes for representing the physical '
                'measurable quantities and the methods to '
                'locate them',
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown"
)
