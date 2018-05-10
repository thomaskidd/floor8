# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

# the button class
from component import *

class Button(Component):

    def __init__( self, xPos, yPos, xSize, ySize, text, command):
        super().__init__(xPos, yPos, xSize, ySize, text)
        self.mCommand = command  # command is set with lambda

    def mouseDown( self, aMousePos ):
        if self.mVisible and self.mClickable:
            if (aMousePos[0] >= self.mx and aMousePos[0] <= (self.mx + self.mxSize)):
                if aMousePos[1] >= self.my and aMousePos[1] <= (self.my + self.mySize):
                    if not self.mClicked:
                        self.mClicked = True
                        self.mColor = self.mClickedColor
                        # if clicked
                        return True

        # if not clicked
        return False

    def mouseUp( self, aMousePos ):
        if self.mVisible and self.mClickable:
            self.mClicked = False
            self.mColor = self.mDefaultColor

            # only execute the command if the user has not moved their mouse off the button
            if (aMousePos[0] >= self.mx and aMousePos[0] <= (self.mx + self.mxSize)):
                if aMousePos[1] >= self.my and aMousePos[1] <= (self.my + self.mySize):
                    self.mCommand()


    # button specific getters and setters

    def getDefaultColor( self ):
        return self.mDefaultColor

    def setDefaultColor( self, color ):
        self.mDefaultColor = color

    def getClickedColor( self ):
        return self.mClickedColor

    def setClickedColor( self, color ):
        self.mClickedColor = color
