from setuptools import setup, find_packages

setup(
    name='Proact AI',
    version='1.0.1',
    description='A library for predicting and blocking suspicious traffic',
    author='Vibe AI',
    author_email='contactvibe615@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'pydantic',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
