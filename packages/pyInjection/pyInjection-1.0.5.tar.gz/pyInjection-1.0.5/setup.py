import setuptools #type: ignore
from os import path

long_description: str = ''
root_path: str = path.abspath(path.dirname(__file__))
with open(path.join(root_path, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setuptools.setup(
    name="pyInjection",
    version="1.0.5",
    author="Joshua Loader",
    author_email="pyInjection@joshloader.com",
    description="Dependency injection container for Python3",
    long_description = long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    package_data={
      'pyInjection': ['py.typed'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
