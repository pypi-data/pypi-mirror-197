#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 10:26:05 2022

@author: luiza
"""

# DRAGGABLE LINE
import matplotlib.lines as lines

line_coord_list = [] 
class draggable_lines:
    def __init__(self, ax, kind, x, ys):
        self.ax = ax
        self.c = ax.get_figure().canvas
        self.o = kind
        self.x = x
        self.line0 = 0

        if kind == "h":
            x = ys
            y = [self.x, self.x]

        elif kind == "v":
            x = [self.x, self.x]
            y = ys
        self.line = lines.Line2D(x, y, picker=5, color ="#12c7e5", linewidth= 3)
        self.ax.add_line(self.line)
        self.c.draw_idle()
        self.sid = self.c.mpl_connect('pick_event', self.clickonline)

    def clickonline(self, event):
        if event.artist == self.line:
            line_coord_list.append(event.artist._label)
            self.follower = self.c.mpl_connect("motion_notify_event", self.followmouse)
            self.releaser = self.c.mpl_connect("button_press_event", self.releaseonclick)
            
    def followmouse(self, event):
        if self.o == "h":
            self.line.set_ydata([event.ydata, event.ydata])
        else:
            self.line.set_xdata([event.xdata, event.xdata])
        self.c.draw_idle()

    def releaseonclick(self, event):
        if self.o == "h":
            self.x = self.line.get_ydata()[0]
        else:
            self.x = self.line.get_xdata()[0]

    
        line_coord_list.append(self.x)
        self.c.mpl_disconnect(self.releaser)
        self.c.mpl_disconnect(self.follower)
    
