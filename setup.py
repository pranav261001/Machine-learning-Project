from setuptools import find_packages, setup
from typing import List
HYPEN_E_DOT = '-e .'

def get_packages(filepath:str)->list[str]:
    '''
    This function will return the packages from requirements.txt file
    '''
    requirements = []
    with open(filepath, 'r') as f:
        
        requirements = f.readlines()
        requirements=[req.replace("\n", " ") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

setup(
    name = "Machine learning project",
    version= '0.0.1',
    author= 'Pranav',
    author_email= 'pranav261001@gmail.com',
    packages= find_packages(),
    install_requires = get_packages('requirements.txt')
)