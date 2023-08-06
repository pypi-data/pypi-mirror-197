from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='allens assignment',
  version='0.0.1',
  description='Basic Mathematical Functions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Muhammad Ahmad Sajid',
  author_email='muhammadahmad.sajid@rakuten.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='functions', 
  packages=find_packages(),
  install_requires=[''] 
)