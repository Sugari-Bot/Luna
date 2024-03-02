from setuptools import setup

setup(
    name="Luna",
    url="https://github.com/Sugari-Bot/Luna",
    author="AmazingAkai",
    author_email="akai.is.amazing@gmail.com",
    version="2.7.0",
    packages=[
        "luna",
        "luna.adapter",
        "luna.block",
        "luna.interface",
    ],
    requires=["discord.py", "expr.py"],
)
