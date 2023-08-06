import setuptools

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extract-samples",
    version="1.0.3",
    author="Hyeonjinkk",
    author_email="ilhj1228@gmail.com",
    description="random sample each file path",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/schooldevops/python-tutorials",
    # project_urls={
    #     "Bug Tracker": "https://github.com/schooldevops/python-tutorials/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where=""),
    python_requires=">=3.6",
)
