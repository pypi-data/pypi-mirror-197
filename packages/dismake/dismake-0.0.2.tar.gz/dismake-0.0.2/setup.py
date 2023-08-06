from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt', 'r') as file:
    requirements = file.read().split('/n')
setup(
    name='dismake',
    version='0.0.2',
    author="Pranoy Majumdar",
    author_email="officialpranoy2@gmail.com",
    description="None",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PranoyMajumdar/dismake",
    project_urls={
        "Homepage": "https://github.com/PranoyMajumdar/dismake"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
    license="MIT",
    install_requires=requirements

)