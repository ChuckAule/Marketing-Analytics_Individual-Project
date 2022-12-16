from setuptools import setup, find_packages

setup(
    author="Valentina Mkhitaryan",
    description="A package for SNA for community detection",
    name="MySNA",
    version="0.1.0",
    packages=find_packages(include=["MySNA", "MySNA.*"]),
    install_requires=["networkx", "operator", "python-louvain", "matplotlib"],
)

