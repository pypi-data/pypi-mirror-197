# SPDX-FileCopyrightText: Copyright (c) Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
from gauge import gauge

display = board.DISPLAY

gauge = gauge(
    50,
    50,
    50,
    250,
    scale_range=[0, 100],
    tick_color=0x440044,
    background_color=0x44FF44,
)

display.show(gauge)


i = 20

while True:
    for a in range(5):
        gauge.update(i)
        i = i + 10
        time.sleep(0.0005)
    for a in range(5):
        gauge.update(i)
        i = i - 10
        time.sleep(0.005)
    i = 20
