from setuptools import setup
from setuptools import find_packages

setup(
    name='BGAscraper', ## This will be the name your package will be published with
    version='0.0.1', 
    description='Package for collecting the data from top players on https://www.boardgamearena.com/',
    url='https://github.com/EdCliffe', # Add the URL of your github repo if published 
                                                                   # in GitHub
    author='Ed Cliffe', # Your name
    license='MIT',
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['requests', 'beautifulsoup4', 'bs4', 'selenium', 'email.mime', 'shutil', 'selenium.common.exceptions'], 
                                                     # Make sure to include all external libraries in this argument
)