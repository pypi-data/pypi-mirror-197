from setuptools import setup
from pawdbt.pawdbt_helper_modules import VERSION, AUTHOR, NAME

setup(
    name=NAME,
    version=VERSION,
    description="Bespoke automation for documenting dbt models",
    author=AUTHOR,
    author_email="dan@dans.design",
    url="https://github.com/dan-wils0n/pawdbt",
    license='MIT',
    packages=['pawdbt'],
    install_requires=[
        'argparse',
        'tqdm',
        'prettytable',
        'halo'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': [
            'pawdbt = pawdbt:main_yaml',
        ]
    }
)