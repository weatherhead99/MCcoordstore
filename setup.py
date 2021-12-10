from setuptools import setup, find_packages

setup(name="MCcoordstore",
      version="0.0.1dev",
      description="simple coordinate store for minecraft",
      author="Dan Weatherill",
      author_email="dan.weatherill@cantab.net",
      packages = find_packages(),
      include_package_data = True,
      install_requires = ["flask",
                          "flask_sqlalchemy",
                          "Flask-WTF",
                          "Flask-login",
                          "matplotlib",
                          "numpy",
                          "mpld3",
                          "werkzeug",
                          "flask-migrate"]
      )