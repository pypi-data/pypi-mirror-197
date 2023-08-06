from setuptools import setup, find_packages

print(find_packages())

requires = [
    'requests>=2.27.1',
    'loguru>=0.6.0',
    'lxml==4.6.3',
    'pydantic==1.9.1',
    'tqdm==4.62.2',
]


setup(
    name="Encrawler",
    version="0.1.18",
    packages=find_packages(),
    description="fix search method paramers",
    long_description="a search engine crawler for bing",
    author="phimes",
    author_email="phimes@163.com",
)
