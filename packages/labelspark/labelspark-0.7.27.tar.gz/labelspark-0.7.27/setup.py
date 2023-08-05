from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='labelspark',
      version='0.7.27',
      packages=find_packages(),
      url='https://github.com/Labelbox/LabelSpark.git',
      description='Labelbox Connector for Databricks',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=["labelbox[data]", "pyspark", "packaging", "labelbase"],
      extras_require={'dev': ['pylint']})
