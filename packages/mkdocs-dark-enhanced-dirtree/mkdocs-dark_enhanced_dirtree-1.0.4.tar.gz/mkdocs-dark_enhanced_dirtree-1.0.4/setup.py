from setuptools import setup, find_packages

# https://pypi.org/project/mkdocs-dark-minimal-dirtree

VERSION = "1.0.4"

setup(
    name="mkdocs-dark_enhanced_dirtree",
    version=VERSION,
    url="https://github.com/Jakkins/dark_enhanced_dirtree",
    license="MIT License",
    description="MkDocs theme to praise the holy (dir) tree",
    author="jakkins",
    author_email="sjakkins@proton.me",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "mkdocs.themes": [
            "dark_enhanced_dirtree = dark_enhanced_dirtree",
        ]
    },
    zip_safe=False,
)
