from setuptools import setup, find_packages

setup(
    name='dng-to-cube',
    version='1.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dng-to-cube = dng_to_cube:main'
        ]
    },
    install_requires=[

    ],
    license='MIT',
    long_description=open('README.md').read(),
)
