import setuptools

with open('requirements.txt') as fid:
    requires = [line.strip() for line in fid]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sculpture",
    version="0.1.0",
    author="Xian-Yun Tang",
    author_email="xt1800i@gmail.com",
    description="A small model api template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
