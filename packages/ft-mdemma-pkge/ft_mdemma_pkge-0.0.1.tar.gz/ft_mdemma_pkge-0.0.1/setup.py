import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ft_mdemma_pkge",
    version="0.0.1",
    description="A sample test package",
    author="mdemma",
    author_email="mdemma@42.fr",
    url="https://github.com/mdemma/ft_package",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),

)