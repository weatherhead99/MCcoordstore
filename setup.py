from setuptools import setup, find_packages

setup(name="MCcoordstore",
      version="0.0.1dev",
      description="simple coordinate store for minecraft",
      author="Dan Weatherill",
      author_email="dan.weatherill@cantab.net",
      packages = find_packages(),
      install_requires = ["flask",
                          "flask_sqlalchemy",
                          "matplotlib",
                          "numpy",
                          "mpld3"]
      
      )