from setuptools import find_packages, setup

setup(
    name='Medical-Chatbot',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.md').read(),
)