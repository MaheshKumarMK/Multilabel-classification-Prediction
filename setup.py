from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_list:List[str]=[]
    with open ("requirements.txt") as requirement_file:
        requirement_list=requirement_file.readlines()
        requirement_list=[req_list.replace('\n', '') for req_list in requirement_list]
        if "-e ." in requirement_list:
            requirement_list.remove("-e .")
        return requirement_list


setup(
    name="Restaurant-rating-prediction",
    version="0.0.1",
    author="Mahesh Kumar",
    author_email="maheshmkvb92@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)