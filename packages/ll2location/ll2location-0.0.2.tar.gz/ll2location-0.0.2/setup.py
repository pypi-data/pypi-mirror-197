import setuptools
# f = open("./requirements.txt", "r")
# def process(txt):
#     return txt.replace("\n", "")
# requirements = list(map(process, f.readlines()))
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

requirements = ["geopandas",\
"shapely",\
"requests",\
"beautifulsoup4"]
setuptools.setup(
    name="ll2location",
    version="0.0.2",
    author="Trương Xuân Linh",
    author_email="truonglinh1342001@gmail.com",
    description="ll2location",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/truong-xuan-linh/ll2location",
    package_data={'': ['*.json', '*.yml']},
    install_requires= requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)