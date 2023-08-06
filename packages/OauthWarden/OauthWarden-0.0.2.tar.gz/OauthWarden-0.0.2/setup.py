from setuptools import setup, find_packages

setup(
    name='OauthWarden',
    version='0.0.2',
    description='Python Package for Twitch requests',
    author='Yokozuna',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
    ],
)