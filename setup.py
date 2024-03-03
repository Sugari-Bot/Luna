import re

from setuptools import setup

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

with open("luna/__init__.py", encoding="utf-8") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(),
        re.MULTILINE,
    )

if not version:
    raise RuntimeError("version is not set")


setup(
    name="luna.py",
    author="AmazingAkai",
    url="https://github.com/AmazingAkai/luna.py",
    version=version.group(1),
    packages=[
        "luna",
        "luna.adapter",
        "luna.block",
        "luna.interface",
    ],
    license="MIT",
    description="An easy drop in user-provided Templating system. ",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8.0",
)
