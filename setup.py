try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='transcoder',
      version='0.1',
      description='Integration library for the Nex-Tech transcoder',
      author='Austin Gabel',
      author_email='agabel@gmail.com',
      url='https://github.com/nex-tech/TranscoderPy',
      license="MIT License",
      install_requires=['requests>=1.0'],
      packages=['transcoder'],
      platforms='any',
)

