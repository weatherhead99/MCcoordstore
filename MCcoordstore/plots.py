#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 19:05:14 2021

@author: danw
"""

import matplotlib.pyplot as plt
import mpld3
from typing import List, Union
import numpy as np

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
    

    
