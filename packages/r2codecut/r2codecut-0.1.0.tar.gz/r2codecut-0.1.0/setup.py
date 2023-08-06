from setuptools import setup
from setuptools.command.install import install

class CustomInstall(install):

    def run(self):
        install.run(self)
        self.__post_install()

    def __post_install(self):
        import nltk
        nltk.download("averaged_perceptron_tagger")

setup(
    name="r2codecut",
    version="0.1.0",
    description="Identify Object File boundaries in binary files",
    url="https://github.com/FernandoDoming/r2codecut",
    author="Fernando Domínguez",
    author_email="fernando.dom.del@gmail.com",
    license="GNU GPL v3",
    packages=[
        "r2codecut",
    ],
    install_requires=[
        "nltk>=3.8.1",
        "r2pipe>=1.6.3",
        "r2magicstrings>=0.1.0",
        "ida2r2>=0.1.0",
    ],
    cmdclass={"install": CustomInstall},
    entry_points = {
        "console_scripts": ["r2codecut=r2codecut.lfa:main"]
    },

    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ]
)