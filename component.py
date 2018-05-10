# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

# parent class for all interactive gui components - mainly buttons
import pygame as pg
from settings import *

class Component:

    # creates all the default values for all components
    def __init__( self, xPos, yPos, xSize, ySize, text ):
        self.mx = xPos
        self.my = yPos
        self.mxSize = xSize
        self.mySize = ySize
        self.mSquare = False
        self.mResizable = True

        # font related
        self.mFontSize = 30
        self.mFont = pg.font.SysFont("Georgia", self.mFontSize)
        self.mText = text
        self.mSurface = self.mFont.render(text, False, (0, 0, 0))
        self.mMinFontSize = 10
        self.mMaxFontSize = 40

        # graphical
        self.mVisible = True
        self.mVisibleToggle = True
        self.mClickedColor = Settings.YELLOW
        self.mDefaultColor = Settings.LIGHTGREY
        self.mColor = self.mDefaultColor
        self.mMinXSize = 80
        self.mMinYSize = 55
        self.mMaxXSize = 500
        self.mMaxYSize = 200
        # these hold the x and y sizes unadjusted for min/max limitations
        self.mRealXSize = self.mxSize
        self.mRealYSize = self.mySize

        # functionality
        self.mClicked = False
        self.mClickable = True

    def draw( self, aScreen ):
        if self.mVisible:
            pg.draw.rect(aScreen, self.mColor, (self.mx, self.my, self.mxSize, self.mySize), 0)
            aScreen.blit(self.mSurface, (self.mx+5, self.my+5))

    # getters and setters

    # location and size
    def setLocation( self, x, y ):
        self.mx = x
        self.my = y

    def getLocation( self ):
        return (self.mx, self.my)

    def setSize( self, xSize, ySize ):
        if self.isResizable():
            if self.isSquare():
                ySize = xSize

            self.setRealSize(xSize, ySize)
            self.mxSize = min(max(xSize, self.mMinXSize), self.mMaxXSize)
            self.mySize = min(max(ySize, self.mMinYSize), self.mMaxYSize)

    def getSize( self ):
        return (self.mxSize, self.mySize)

    def setRealSize( self, xSize, ySize ):
        self.mRealXSize = xSize
        self.mRealYSize = ySize

    def getRealSize( self ):
        return (self.mRealXSize, self.mRealYSize)

    def setMinSize( self, xSize, ySize):
        self.mMinXSize = xSize
        self.mMinYSize = ySize

    def getMinSize( self ):
        return (self.mMinXSize, self.mMinYSize)

    def setMaxSize( self, xSize, ySize):
        self.mMaxXSize = xSize
        self.mMaxYSize = ySize

    def getMaxSize( self ):
        return (self.mMaxXSize, self.mMaxYSize)

    def setSquare( self, bool ):
        self.mSquare = bool

    def isSquare( self ):
        return self.mSquare

    def setResizability( self, bool ):
        self.mResizable = bool

    def isResizable( self ):
        return self.mResizable

    # text and font
    def setTextDisplacement( self, x, y ):
        self.mxDisplacement = x
        self.myDisplacement = y

    def setText( self, text ):
        self.mText = text
        self.mSurface = self.mFont.render(self.mText, False, (0, 0, 0))

    def getText( self ):
        return self.mText

    def setFont( self, font ):
        self.mFont = font

    def setFontSize( self, size ):
        self.mFontSize = size
        self.mFont = pg.font.SysFont("Georgia", int(min(max(size, self.mMinFontSize), self.mMaxFontSize)))
        self.mSurface = self.mFont.render(self.mText, False, (0, 0, 0))

    def getFontSize( self ):
        return self.mFontSize

    # visibility
    def setVisible( self, bool ):
        self.mVisible = bool

    def getVisible( self ):
        return self.mVisible

    # set visibility toggle
    def setVisibleToggle( self, bool ):
        self.mVisibleToggle = bool

    def getVisibleToggle( self ):
        return self.mVisibleToggle

    # visibility hotkey
    def switchVisibility( self ):
        if self.getVisibleToggle():
            if self.getVisible():
                self.setVisible(False)
            else:
                self.setVisible(True)

    # clickability
    def setClickable( self, bool ):
        self.mClickable = bool

    def getClickable( self ):
        return self.mClickable

    def switchClickability( self ):
        if self.getClickable():
            self.setClickable(False)
        else:
            self.setClickable(True)

    # movability
    def setMovable( self, bool ):
        self.mMoveable = bool

    def getMovable( self ):
        return self.mMoveable