# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

# the label class
from component import *

class Label(Component):

    def __init__( self, xPos, yPos, xSize, ySize, text):
        super().__init__(xPos, yPos, xSize, ySize, text)
        self.mClickable = False # just to be explicit