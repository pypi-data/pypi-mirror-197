from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='potato-annotation',
    version='1.2.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'potato = potato.cli:potato',
        ],
    },
    author="Jiaxin Pei",
    author_email="pedropei@umich.edu",
    description="Potato text annotation tool",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown"
)
