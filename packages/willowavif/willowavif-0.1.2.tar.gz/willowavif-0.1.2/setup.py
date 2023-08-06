import setuptools

description = "Plugin for willow to enable AVIF support"

try:
    with open("README.md", encoding="utf-8") as fh:
        long_description = fh.read()
except OSError:
    long_description = description

setuptools.setup(
    name="willowavif",
    version="0.1.2",
    author="Ben Gosney",
    author_email="bengosney@googlemail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bengosney/willow-avif",
    project_urls={
        "Bug Tracker": "https://github.com/bengosney/willow-avif/issues",
    },
    install_requires=[
        "Pillow",
        "Willow",
        "pillow-avif-plugin",
        "wrapt",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
