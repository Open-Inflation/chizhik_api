from setuptools import setup, find_packages

setup(
    name='chizhik_api',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'playwright',
        'playwright_stealth',
    ],
    author='Miskler',
    description='A Python API client for Chizhik catalog',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Open-Inflation/chizhik_api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
