from setuptools import find_packages, setup

# Read the contents of requirements.txt and split it into lines

def get_requirements(file_path:str)->list[str]:
    requirements = []
    with open(file_path, 'r') as file:
        req_1 = file.read().splitlines()
        for i in req_1:
            if i == "-e .":
                continue
            else:
                requirements.append(i)
    return requirements

setup(
    name='RegressionProject',
    version='0.0.0',
    author="Abhishek",
    author_email="abhishekdutta.9579@gmail.com",
    install_requires = get_requirements("requirements.txt"),
    packages = find_packages()

)