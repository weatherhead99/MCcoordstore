#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


"""
Created on Thu Dec  9 19:05:14 2021

@author: danw
"""

import matplotlib
import matplotlib.pyplot as plt
import mpld3
from typing import List, Union
import numpy as np

matplotlib.use("template")


class LocationsPlot:
    def __init__(self, **plotkwargs):
        self.fig, self.ax = plt.subplots(1,1, **plotkwargs)
        self.scatter = None
        self.xdat = []
        self.zdat = []
        self.syms = []
        self.colors = []
        self._needs_render: Union[bool,None] = None
        self._rendered_html = None

    def update_plot(self):
        if self.scatter is None:
            self.scatter = self.ax.scatter(self.xdat, self.zdat)
        else:
            dat = np.vstack((self.xdat, self.zdat))
            self.scatter.set_offsets(dat)
        
        self._needs_render = True
        
    @property
    def rendered_html(self) -> str:
        if self._needs_render is None:
            raise RuntimeError("plot needs to be updated first")
        if self._needs_render:
            self._rendered_html = mpld3.fig_to_html(self.fig)
            self._needs_render = False
        return self._rendered_html

        
    
        
if __name__ == "__main__":
    plt.close("all")
    newplot = LocationsPlot()
    
    newplot.xdat = np.random.normal(0., 1., 5)
    newplot.zdat = np.random.normal(0, 1, 5)
    
    newplot.update_plot()
    

    
