# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

import pygame as pg

gCursor = (
"                ",
"                ",
"                ",
"                ",
"       XX       ",
"       XX       ",
"       XX       ",
"    XXX  XXX    ", # middle
"    XXX  XXX    ", # middle
"       XX       ",
"       XX       ",
"       XX       ",
"                ",
"                ",
"                ",
"                ",
)

gCursor1 = (
    "      .  .      ",
    "     .X  X.     ",
    "    .XX  XX.    ",
    "    .XX  XX.    ",
    "  ....X  X....  ",
    " .XX.XX  XX.XX. ",
    ".XXXXX    XXXXX.",
    "                ",# middle
    "                ",# middle
    ".XXXXX    XXXXX.",
    " .XX.XX  XX.XX. ",
    "  ....X  X....  ",
    "    .XX  XX.    ",
    "    .XX  XX.    ",
    "     .X  X.     ",
    "      .  .      ",
)

def createCursorFromStrings():
    vXor, vAnd = pg.cursors.compile( gCursor1 )

    pg.mouse.set_cursor( ( 16, 16 ), ( 7, 7 ), vXor, vAnd )