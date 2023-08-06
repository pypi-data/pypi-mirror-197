from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='dgec2',  # 包名
      version='3.1.4',  # 版本号
      description='To complete the measurement of digital economy',
      long_description='Based on the analysis of newspaper text and network dynamics, this index can extract the implied information in newspapers to replace traditional economic data to construct the measurement of digital economy. The advantage of this measure is that it includes both direct hard information and indirect soft factors. In addition, it can dynamically simulate influence indicators to provide suggestions for accurate decision-making of the government',
      author='Y.C.Huang',
      author_email='1658460876@qq.com',
      install_requires=['pandas'],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )