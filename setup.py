# MIT License - Copyright (c) 2025 Robert Cole

setup_text = """from setuptools import setup, find_packages

setup(
    name='btpie-n-the-middle',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'btpie = scripts.btpie:main'
        ]
    },
)
