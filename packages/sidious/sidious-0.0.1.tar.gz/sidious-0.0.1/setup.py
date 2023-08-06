from setuptools import find_packages, setup

setup(
    name="sidious",
    version="0.0.1",
    long_description_content_type="text/markdown",
    description="",
    url="",
    author="Sotetsu KOYAMADA",
    author_email="sotetsu.koyamada@gmail.com",
    keywords="",
    packages=find_packages(),
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    install_requires=["jax"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
)
