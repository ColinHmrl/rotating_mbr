from setuptools import setup, find_packages

setup(
    name='rotating-mbr',
    version='0.1',
    description='Rotating Minimum Bounding Rectangle with cloud points',
    author='Colin_Hmrl',
    author_email='hamerel.co@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8.10',
    ],
)