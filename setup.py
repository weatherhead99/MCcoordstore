#      MCcoordstore - simple web based store for Minecraft points of interest
#      Copyright (C) 2021  Daniel Philip Weatherill

#      This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.

#      This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.

#      You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README").read_text()

setup(name="MCcoordstore",
      version="0.0.1dev",
      description="simple coordinate store for minecraft",
      long_description=README,
      long_description_content_type="text/markdown",
      license="AGPL-3.0-or-later",
      author="Dan Weatherill",
      author_email="dan.weatherill@cantab.net",
      url="https://github.com/weatherhead99/MCcoordstore",
      packages = find_packages(),
      include_package_data = True,
      classifiers = [
          "Development Status :: 2 - Pre-Alpha",
          "Framework :: Flask",
          "License :: OSI Approved :: GNU Affero General Public License v3",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
          ],
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
