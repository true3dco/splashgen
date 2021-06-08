import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="splashgen",
    version="0.0.28",
    description="Create a splash page in less than 20 lines of python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/true3dco/splashgen",
    author="True3D",
    author_email="founders@true3d.live",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Jinja2", "query_string",
                      "urlexpander", "pillow",
                      "python-slugify", "pyhumps"],
    entry_points={
        "console_scripts": [
            "splashgen=splashgen.cli:main",
        ]
    },
    # TODO: Add frontend stuff (but not node_modules nor anything in the gitignore)
    package_data={'splashgen': ['jinja_templates/*.jinja', 'assets/*.png']},
)
