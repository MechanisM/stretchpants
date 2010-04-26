from setuptools import setup, find_packages
import os


setup(name="stretchpants",
      version="0.1.0-devel",
      description="A layer between MongoEngine and ElasticSearch.",
      author="Matt Dennewitz",
      author_email="mattdennewitz@gmail.com",
      license="BSD",
      install_requires=['pymongo', "mongoengine"],
      url="http://mattdennewitz.tumblr.com/",
      packages=["stretchpants"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Environment :: Web Environment",
                   "Framework :: MongoEngine",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Utilities",
                   "Topic :: Database"])