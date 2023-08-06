import os

from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

version = "0.3.0"
circleci_build_number = os.getenv("CIRCLE_BUILD_NUM", "")
if circleci_build_number != "":
    version = f"{version}.dev{circleci_build_number}"

setup(
    name="shaped",
    version=version,
    author="Shaped Team",
    author_email="support@shaped.ai",
    url="https://github.com/shaped-ai/shaped-cli",
    description="A CLI tool for interacting with the Shaped API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["shaped-ai"],
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    packages=find_packages(),
    zip_safe=True,
    install_requires=[
        "typer[all]>=0.7.0",
        "requests>=2.28.1",
        "pydantic>=1.10.2",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.7",
    entry_points={"console_scripts": ["shaped=src.shaped_cli:app"]},
)
