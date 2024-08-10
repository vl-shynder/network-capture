from setuptools import setup, find_packages

setup(
    name='Network Capture',
    version='0.1dev',
    author='Vladyslav Shynder',
    author_email='vl.shynder@gmail.com',
    paclages=find_packages(),
    install_requires=[
        'pyshark',
        'notify-py',
    ],
)