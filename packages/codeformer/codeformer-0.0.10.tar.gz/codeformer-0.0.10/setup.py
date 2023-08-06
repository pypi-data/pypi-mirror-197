from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="codeformer",
    version="0.0.10",
    description="Codeformer python wrapper",
    long_description=long_description,
    url="https://github.com/rohitkhatri/codeformer",
    author="Rohit Khatri",
    author_email="developer.rohitkhatri@gmail.com",
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="codeformer python wrapper",
    packages=find_packages(),
    install_requires=[
        "torchvision",
        "opencv-python",
        "lpips",
        "pyyaml",
    ],
)
