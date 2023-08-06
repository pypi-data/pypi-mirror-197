with open("README.md", encoding="utf8") as readme:
    LONG_DESCRIPTION = readme.read()

from setuptools import setup, find_packages

VERSION = "1.1.10"
DESCRIPTION = "Python wrapper for the TechZApi"

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="techzapi",
    version=VERSION,
    license="MIT",
    author="TechShreyash",
    author_email="techshreyash123@gmail.com",
    long_description_content_type="text/markdown",
    url="https://github.com/TechShreyash/TechZApi",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=[
        "API",
        "TechZApi",
        "TechZAPI",
        "TechZBots",
        "GogoAnime",
        "Anime",
        "AnimeAPI",
    ],
)
