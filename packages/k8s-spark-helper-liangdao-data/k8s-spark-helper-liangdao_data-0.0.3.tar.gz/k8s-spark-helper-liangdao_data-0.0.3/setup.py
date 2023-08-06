import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="k8s-spark-helper-liangdao_data",
  version="0.0.3",
  author="yuchao.li",
  author_email="yuchao.li@liangdao.ai",
  description="Run spark task in k8s",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
