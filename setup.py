# MIT License - Copyright (c) 2025 Robert Cole

from setuptools import setup, find_packages

setup(
    name='btpie-n-the-middle',
    version='0.1.0',
    author='Robert Cole',
    description='Modern Bluetooth Proxy-In-The-Middle (MITM) Tool for Raspberry Pi',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/daedalas1981/btpie-n-the-middle',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Leave empty if system packages like pybluez are installed via apt
        # 'pybluez>=0.23'  # Uncomment only if pip-managed pybluez is tested/needed
    ],
    entry_points={
        'console_scripts': [
            'btpie=scripts.btpie:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
    ],
    python_requires='>=3.7',
)

