from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in estate/__init__.py
from estate import __version__ as version

setup(
	name="estate",
	version=version,
	description="Estate Management App",
	author="Kunle Oduntan	",
	author_email="Kunleoduntan@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
