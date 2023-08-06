import setuptools

with open("README.md", encoding="utf8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="techzapi",
    packages=["techzapi"],
    version="1.1.8",
    license="MIT",
    description="Python Wrapper For TechZApi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TechShreyash",
    author_email="techshreyash123@gmail.com",
    url="https://github.com/TechShreyash/TechZApi",
    keywords=[
        "API",
        "TechZApi",
        "TechZAPI",
        "TechZBots",
        "GogoAnime",
        "Anime",
        "AnimeAPI",
    ],
    install_requires=["requests"],
    zip_safe=False,
)
