from setuptools import setup, find_packages

setup(
    name='conn2combat',
    version='0.1.0',
    author='T. Bryan Jackson',
    author_email='trevorbryanjackson@gmail.com',
    description='A package for parsing .mat files from CONN first-level ROI-to-ROI analyses and preparing data for COMBAT.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/trevorbryanjackson/conn2combat',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)