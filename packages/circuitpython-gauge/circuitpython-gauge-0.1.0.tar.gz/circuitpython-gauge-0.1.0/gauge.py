# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya for Jose D.
#
# SPDX-License-Identifier: MIT
"""
`gauge`
================================================================================

CircuitPython Gauge


* Author(s): Jose D. Montoya

Implementation Notes
--------------------


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


"""

try:
    from typing import Union, Tuple, Optional
except ImportError:
    pass

import displayio
import terminalio
from bitmaptools import draw_line
from vectorio import Polygon
from ulab import numpy as np

__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_Gauge.git"

# pylint: disable=too-many-arguments, too-many-instance-attributes, too-many-locals
# pylint: disable=too-many-statements, unnecessary-comprehension
# pylint: disable=unused-import, import-outside-toplevel, undefined-variable
# pylint: disable=invalid-name, dangerous-default-value


class gauge(displayio.Group):
    """
    scales Class to add different elements to the screen.
    The origin point set by ``x`` and ``y`` properties

    :param int x: origin x coordinate
    :param int y: origin y coordinate
    :param int width: plot box width in pixels. Defaults to 100.
    :param int height: plot box height in pixels. Defaults to 100.
    :param int padding: padding for the scale box in all directions
    :param list|None scale_range: x range limits. Defaults to None

    :param int background_color: background color in HEX. Defaults to black ``0x000000``
    :param int box_color: allows to choose the box line color. Defaults to white ''0xFFFFFF``

    :param int tick_lenght: x axes tick height in pixels. Defaults to 28.
    :param int tick_color: x axes tick height in pixels. Defaults to 0xFFFFFF.
    :param str|None: Argument to locate the ticks. Left, center or all
    :param int pointer_lenght: width of the bar. Defaults to 10.
    :param int scale: scale of the widget


    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 100,
        padding: int = 1,
        scale_range: Optional[list] = [0, 150],
        background_color: int = 0x000000,
        box_color: int = 0xFF8500,
        tick_lenght: int = 28,
        tick_color: int = 0xFFFFFF,
        tick_pos: Optional[str] = None,
        pointer_lenght: int = 10,
        scale: int = 1,
    ) -> None:
        if width not in range(50, 481) and scale == 1:
            print("Be sure to verify your values. Defaulting to width=100")
            width = 100
        if height not in range(50, 321) and scale == 1:
            print("Be sure to verify your values. Defaulting to height=100")
            height = 100
        if x + width > 481:
            print(
                "Modify this settings. Some of the graphics will not shown int the screen"
            )
            print("Defaulting to x=0")
            x = 0
        if y + height > 321:
            print(
                "Modify this settings. Some of the graphics will not shown int the screen"
            )
            print("Defaulting to y=0")
            y = 0

        super().__init__(x=x, y=y, scale=scale)

        self._width = width
        self._height = height

        self.padding = padding

        self.ymin = scale_range[0]
        self.ymax = scale_range[1]
        self._newxmin = padding
        self._newxmax = width - padding

        self._center = (self._newxmax - self._newxmin) // 2

        self._newymin = height - padding
        self._newymax = padding

        self.ticksy = np.array([element for element in range(self.ymin, self.ymax, 10)])

        self._showtext = True

        self._tickcolor = tick_color
        self._pointer_palette = displayio.Palette(2)
        self._pointer_palette.make_transparent(0)
        self._pointer_palette[1] = self._tickcolor
        self.pointer = None
        self._pointer_lenght = pointer_lenght
        self._tick_lenght = tick_lenght
        if tick_pos == "left":
            self._tickpos = self._newxmin
        elif tick_pos == "center":
            self._tickpos = self._center - self._tick_lenght // 2
        else:
            self._tickpos = self._newxmin
            self._tick_lenght = self._width

        self.value = 0

        self._showticks = True

        self._plotbitmap = displayio.Bitmap(width, height, 4)

        self.pointer_size = 6
        self._drawbox()

        self._plot_palette = displayio.Palette(4)
        self._plot_palette[0] = background_color
        self._plot_palette[1] = box_color
        self._plot_palette[2] = self._tickcolor

        self.points = None
        self.y0 = None
        self.x0 = None
        self.y1 = None
        self.x1 = None

        self.append(
            displayio.TileGrid(
                self._plotbitmap, pixel_shader=self._plot_palette, x=0, y=0
            )
        )
        self._draw_ticks()
        self._draw_pointer()

    def _drawbox(self) -> None:
        """
        Draw the plot box

        :return: None

        """

        draw_box = [True, True, True, True]

        if draw_box[0]:
            # y axes line
            draw_line(
                self._plotbitmap,
                self.padding,
                self.padding,
                self.padding,
                self._height - self.padding,
                1,
            )
        if draw_box[1]:
            draw_line(
                self._plotbitmap,
                self.padding,
                self._height - self.padding,
                self._width - self.padding,
                self._height - self.padding,
                1,
            )
        if draw_box[2]:
            draw_line(
                self._plotbitmap,
                self._width - self.padding,
                self.padding,
                self._width - self.padding,
                self._height - self.padding,
                1,
            )
        if draw_box[3]:
            draw_line(
                self._plotbitmap,
                self.padding,
                self.padding,
                self._width - self.padding,
                self.padding,
                1,
            )

    @staticmethod
    def transform(
        oldrangemin: Union[float, int],
        oldrangemax: Union[float, int],
        newrangemin: Union[float, int],
        newrangemax: Union[float, int],
        value: Union[float, int],
    ) -> Union[float, int]:
        """
        This function converts the original value into a new defined value in the new range

        :param int|float oldrangemin: minimum of the original range
        :param int|float oldrangemax: maximum of the original range
        :param int|float newrangemin: minimum of the new range
        :param int|float newrangemax: maximum of the new range
        :param int|float value: value to be converted

        :return int|float: converted value

        """

        return (
            ((value - oldrangemin) * (newrangemax - newrangemin))
            / (oldrangemax - oldrangemin)
        ) + newrangemin

    def _draw_ticks(self) -> None:
        """
        Draw ticks in the plot area

        """

        ticksynorm = np.array(
            self.transform(
                self.ymin, self.ymax, self._newymin, self._newymax, self.ticksy
            ),
            dtype=np.int16,
        )

        for i, tick in enumerate(ticksynorm):
            if i == 0:
                continue
            draw_line(
                self._plotbitmap,
                self._newxmin + self._tickpos,
                tick,
                self._newxmin + self._tick_lenght + self._tickpos,
                tick,
                2,
            )
            if self._showtext:
                self.show_text(
                    "{:.2f}".format(self.ticksy[i]), self._newxmin, tick, (1.0, 0.5)
                )

    def show_text(
        self, text: str, x: int, y: int, anchorpoint: Tuple = (0.5, 0.0)
    ) -> None:
        """

        Show desired text in the scree
        :param str text: text to be displayed
        :param int x: x coordinate
        :param int y: y coordinate
        :param Tuple anchorpoint: Display_text anchor point. Defaults to (0.5, 0.0)
        :return: None
        """
        if self._showtext:
            from adafruit_display_text import bitmap_label

            text_toplot = bitmap_label.Label(terminalio.FONT, text=text, x=x, y=y)
            text_toplot.anchor_point = anchorpoint
            text_toplot.anchored_position = (x, y)
            self.append(text_toplot)

    def _draw_pointer(self):
        self.x0 = self._center - self._pointer_lenght // 2
        self.y0 = self._newymin
        self.x1 = self._center + self._pointer_lenght // 2
        self.y1 = self._newymin - self.pointer_size - self.value

        self.points = [
            (self.x0, self.y0),
            (self.x1, self.y0),
            (self.x1, self.y1),
            (self.x0, self.y1),
        ]
        self.pointer = Polygon(
            pixel_shader=self._pointer_palette,
            points=self.points,
            x=0,
            y=0,
            color_index=1,
        )
        self.append(self.pointer)

    def update(self, new_value):
        """
        Function to update gauge value
        :param new_value: value to be updated
        :return: None
        """
        self.value = int(
            self.transform(
                self.ymin, self.ymax, self._newymax, self._newymin, new_value
            )
        )
        if self.value >= self._newymin - self.pointer_size:
            self.value = self._newymin - self.pointer_size
        self.y1 = self._newymin - self.pointer_size - self.value
        self.points = [
            (self.x0, self.y0),
            (self.x1, self.y0),
            (self.x1, self.y1),
            (self.x0, self.y1),
        ]
        self.pointer.points = self.points
