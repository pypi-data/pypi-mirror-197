from setuptools import setup, find_packages

setup(
    name='fileextractor',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
    ],
    entry_points={
        # Add any entry points here
    },
    author='Charleen lozi',
    author_email='clozymwangs@gmail.com',
    description='excel to yaml files extractor',
    long_description='Package to extract rasa content data files from excel sheets into respective yaml files. The data being extracted is nlu training data and responses for respective languages, english and swahili ,and stories data into their respective yaml files.',
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/your_package',
    # project_urls={
    #     'Bug Tracker': 'https://github.com/your_username/your_package/issues',
    #     'Documentation': 'https://your_package.readthedocs.io',
    #     'Source Code': 'https://github.com/your_username/your_package',
    # },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)
