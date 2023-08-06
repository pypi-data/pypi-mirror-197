from setuptools import setup, find_packages
import os
with open("README.md", "r") as fh:
  long_description = fh.read()
  
setup(
  name='simsimix',
  packages=find_packages(),
  include_package_data=True,
  version="1.0.0",
  description= '''World first popular Chatbot for daily conversation (Service launched in 2002). A unique daily conversation with diversity, fun and vitality. Service provided with 130 million sets of daily small talks in 81 languages compiled through more than 20 million panels. Service in 81 languages. More than 350 million cumulative users worldwide. (Based on June-2018), Records of more than 200 million times of responses made per day.''',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='akxvau',
  author_email='akxvau@gmail.com',
  install_requires=['requests'],
  keywords=["simsimi","simi","chatBot","chat with simi","simsimi module","simisimi python","simi module","simi py","akxvau","toxinum","simi chatting module","simisimi official"],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    'Environment :: Console'],
  license='MIT',
  python_requires='>=3.9.5'
  )