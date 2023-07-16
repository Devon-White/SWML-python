from setuptools import setup, find_packages

setup(
    name='swml-python',
    version='0.1',
    packages=find_packages(),
    description='A Python wrapper for the new SignalWire product SWML (SignalWire MarkUp Language) ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Devon White',
    author_email='devon.white@signalwire.com',
    url='https://github.com/Devon-White/SWML-python',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
