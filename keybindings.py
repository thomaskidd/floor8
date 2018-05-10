# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

import pygame as pg
from enum import Enum

# this is where we define the actions that the keys map to
class EventActions( Enum ):
    NoEvent = 0
    Select = 1
    Deselect = 2
    ZoomIn = 4
    ZoomOut = 5
    ScrollLeft = 100
    ScrollUp = 101
    ScrollDown = 102
    ScrollRight = 103
    EndTurn = 1000
    SaveGame = 10000
    LoadGame = 10001
    OpenConsole = 100000

# this is where all the base key bindings are stored
# multiple keys can do the same action,
# BUT a key can only map to one action
regKeybindingDict = {
    # mouse bindings here, FYI event.button returns ints as follows
    # 1 - left click, 2 - middle click
    # 3 - right click, 4 - scroll up
    # 5 - scroll down
    1 : EventActions.Select,
    2 : EventActions.NoEvent,
    3 : EventActions.Deselect,
    4 : EventActions.ZoomIn,
    5 : EventActions.ZoomOut,
    pg.K_a : EventActions.ScrollLeft,
    pg.K_w : EventActions.ScrollUp,
    pg.K_s : EventActions.ScrollDown,
    pg.K_d : EventActions.ScrollRight,
    pg.K_RETURN : EventActions.EndTurn,
    pg.K_t : EventActions.SaveGame,
    pg.K_y : EventActions.LoadGame,
    pg.K_BACKQUOTE : EventActions.OpenConsole,
}