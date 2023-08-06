import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SSPM",
    version="1.2.1",
    author="Steven Nix",
    license='GNU LGPLv3',
    author_email="stevencnix@gmail.com",
    description="SSPM simple plugin manger based on YAPSY",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/stevencnix/sspm",
    download_url="https://gitlab.com/stevencnix/sspm/-/archive/v1.2.1/sspm-v1.2.1.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)