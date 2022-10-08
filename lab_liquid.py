#!/usr/bin/env python
# -*- encoding: utf-8 -#-

'''
interactive_xy.py

Demonstrate use of axidraw module in "interactive" mode.

Run this demo by calling: python interactive_xy.py


(There is also a separate "plot" mode, which can be used for plotting an
SVG file, rather than moving to various points upon command.)

AxiDraw python API documentation is hosted at: https://axidraw.com/doc/py_api/

'''


'''
About this software:

The AxiDraw writing and drawing machine is a product of Evil Mad Scientist
Laboratories. https://axidraw.com   https://shop.evilmadscientist.com

This open source software is written and maintained by Evil Mad Scientist
to support AxiDraw users across a wide range of applications. Please help
support Evil Mad Scientist and open source software development by purchasing
genuine AxiDraw hardware.

AxiDraw software development is hosted at https://github.com/evil-mad/axidraw

Additional AxiDraw documentation is available at http://axidraw.com/docs

AxiDraw owners may request technical support for this software through our 
github issues page, support forums, or by contacting us directly at:
https://shop.evilmadscientist.com/contact



Copyright 2020 Windell H. Oskay, Evil Mad Scientist Laboratories

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''






'''

Interactive mode is a mode of use, designed for plotting individual motion
segments upon request. It is a complement to the usual plotting modes, which
take an SVG document as input.

So long as the AxiDraw is started in the home corner, moves are limit checked,
and constrained to be within the safe travel range of the AxiDraw.



Recommended usage:

ad = axidraw.AxiDraw() # Initialize class
ad.interactive()            # Enter interactive mode

[Optional: Apply custom settings]

ad.connect()                # Open serial port to AxiDraw 

[One or more motion commands]
[Optional: Update settings, followed by calling update().]

ad.disconnect()             # Close connection to AxiDraw


The motion commands are as follows:

goto(x,y)    # Absolute XY move to new location
moveto(x,y)  # Absolute XY pen-up move. Lift pen before moving, if it is down.
lineto(x,y)  # Absolute XY pen-down move. Lower pen before moving, if it is up.

go(x,y)      # XY relative move.
move(x,y)    # XY relative pen-up move. Lift pen before moving, if it is down.
line(x,y)    # XY relative pen-down move. Lower pen before moving, if it is up.

penup()      # lift pen
pendown()    # lower pen


Utility commands:

interactive()   # Enter interactive mode
connect()       # Open serial connection to AxiDraw. Returns True if connected successfully.
update()        # Apply changes to options
disable()       # Disable XY motors, for example to manually move carriage to home position. 
disconnect()    # Terminate serial session to AxiDraw. (Required.)




The available options are as follows:

options.speed_pendown   # Range: 1-110 (percent). 
options.speed_penup     # Range: 1-110 (percent). 
options.accel           # Range: 1-100 (percent). 
options.pen_pos_down    # Range: 0-100 (percent). 
options.pen_pos_up      # Range: 0-100 (percent).
options.pen_rate_lower  # Range: 1-100 (percent).
options.pen_rate_raise  # Range: 1-100 (percent).
options.pen_delay_down  # Range: -500 - 500 (ms).
options.pen_delay_up    # Range: -500 - 500 (ms).
options.const_speed     # True or False. Default: False
options.units	        # Range: 0-1.  0: Inches (default), 1: cm
options.model           # Range: 1-3.   1: AxiDraw V2 or V3 ( Default)
                        #               2: AxiDraw V3/A3
                        #               3: AxiDraw V3 XLX
options.port            # String: Port name or USB nickname
options.port_config     # Range: 0-1.   0: Plot to first unit found, unless port specified. (Default)
                        #               1: Plot to first unit found

One or more options can be set after the interactive() call, and before connect() 
for example as:

ad.options.speed_pendown = 75



All options except port and port_config can be changed after connect(). However,
you must call update() after changing the options and before calling any
additional motion commands.


'''

import sys
from time import sleep
from pyaxidraw import axidraw

ad = axidraw.AxiDraw() # Initialize class
firsthole_x = 0
firsthole_y = 0
unit_x = 0.8
unit_y = 0.825
print("Starting X: ")
input(firsthole_x)
print("Starting Y: ")
input(firsthole_y)
print("X unit: ")
input(unit_x)
print("Y unit: ")
input(unit_y)
def press():
    ad.usb_command("S2,11650,6\r\r")
def release():
    ad.usb_command("S2,21000,6\r\r")
def neutral():
    ad.usb_command("S2,19000,6\r\r")
def origin(a=0, b=0):
    ad.goto(firsthole_x - a, firsthole_y - b)
    ad.penup()
    neutral()
def changePipetTo(x):
    # 1-3 from size
    if x == 1:   
        ad.penup()
        ad.goto(10,1)
        ad.pendown()
    elif x == 2:
        ad.penup()
        ad.goto(10,3)
        ad.pendown()
    elif x == 3:
        ad.penup()
        ad.goto(10,5)
        ad.pendown()
    else:
        x = 1
        changePipetTo(x)
def pipette(x1, x2, y1, y2):
    ad.goto(x1 * unit_x, y1 * unit_y)
    ad.pendown()
    press()
    sleep(1)
    neutral()
    sleep(1)
    ad.penup()
    ad.goto(x2 * unit_x, y2 * unit_y)
    sleep(1)
    ad.pendown()
    press()
    sleep(1)
    ad.penup()
    origin()
def changetip():
    press()
    sleep(1)
    ad.goto(7,7) # tip disposal place
    release()
    sleep(3.25)
    ad.goto(0, 0)
    neutral()
    sleep(1)
    ad.goto(17 * unit_x + 0.1, firsthole_y)
    ad.pendown()
    sleep(1)
    ad.penup()

ad.interactive()            # Enter interactive mode
connected = ad.connect()    # Open serial port to AxiDraw 
if not connected:
    sys.exit() # end script

ad.options.pen_pos_down = 0     # minimum pen posture
ad.options.pen_pos_up = 100     # maximum pen posture
ad.options.units = 1        # set working units to cm.
#ad.options.speed_pendown = 10     # set pen-down speed to slow
ad.options.pen_rate_lower = 60  # Set pen down percentage
#ad.options.speed_penup = 110 # set pen up fast
ad.options.pen_rate_raise = 100 # set pen up percentage
ad.options.pen_delay_down = 500 # max delay after pen down  
ad.update()

#=====================START CODE================================================================================================================================================
origin()   
ad.pendown()
ad.disconnect() 
pipette(0,0,0,3)
changetip()
pipette(1,0,0,3)
changetip()
pipette(2,0,0,3)
changetip()
pipette(3,0,0,3)
changetip()
pipette(4,0,0,3)
changetip()
pipette(5,0,0,3)
changetip()
changePipetTo(2)
pipette(6,0,0,3)
changetip()
changePipetTo(3)
pipette(6,0,0,3)
changetip()
origin()
ad.disconnect()
#===============================================================================================================================================================================
