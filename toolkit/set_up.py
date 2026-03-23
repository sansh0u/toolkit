from setuptools import setup, find_packages

setup(
    name="mycli-package",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "runcli = cli:app",  # Typer 会自动处理这个入口
        ],
    },
)