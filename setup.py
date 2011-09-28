from setuptools import setup

setup(name='django-reuse',
      version='0.38',
      description="Yet another collection of components commonly used for Django sites",
      long_description="",
      author='Markus Kaiserswerth',
      author_email='mkai@sensun.org',
      license='GPL',
      packages=['reuse'],
      zip_safe=False,
      install_requires=['django'],
)
