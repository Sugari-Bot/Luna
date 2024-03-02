import re

from setuptools import setup

version = None
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
    install_requires=["discord.py", "expr.py"],
    python_requires=">=3.8.0",
)
