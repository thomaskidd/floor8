# the class to handle the tile map editor
import pygame as pg
from settings import Settings
from component import *
from button import Button

class TileType():
    GRASS = "g"
    FOREST = "f"
    WATER = "w"
    PLAIN = "p"
    CITY = "z"

class TileEditor():

    def __init__( self, parent, xPos, yPos, xSize, ySize ):
        self.mParent = parent

        # tile related member variables
        self.mSize = Settings.WIDTH / 32
        self.mBuffer = 2
        self.mTiles = [[TileType.GRASS for x in range(xSize)] for y in range(ySize)]

        # create and load a 2d array of buttons
        self.mButtonMap = [[0 for x in range(xSize)] for y in range(ySize)]
        self.mButtons = []
        self.generateTileButtons(xPos, yPos)

    # tile map loading
    def generateTileButtons( self, axPos, ayPos):

        for y in range(len(self.mButtonMap)):
            for x in range(len(self.mButtonMap[y])):
                self.mButtonMap[x][y] = Button(axPos + x*(self.mSize+self.mBuffer), ayPos + y*(self.mSize+self.mBuffer), self.mSize, self.mSize, TileType.GRASS, self.localScopeWrapper(x, y))
                self.mButtonMap[x][y].setMinSize(10, 10)
                self.mButtonMap[x][y].setFontSize(Settings.WIDTH / 64) # size 20
                self.mButtons.append(self.mButtonMap[x][y])

    def localScopeWrapper( self, x, y ):
        # lambda passes by reference, we need it to pass by value in this case
        return lambda: self.changeTile(x, y)

    # drawing and graphical
    def drawAll( self, aScreen):
        for button in self.mButtons:
            button.draw(aScreen)

    def changeTile( self, aX, aY ):
        self.mButtonMap[aX][aY].setText(self.mParent.getSelectedTileType()) # this will be changed to the sprite image
        self.mTiles[aX][aY] = self.mParent.getSelectedTileType()

    def resizeComponents(self, aOldWidth, aOldHeight, aNewWidth, aNewHeight):

        # change the location of the entire map as one
        vPos = self.mButtons[0].getLocation()
        vSize = self.mButtons[0].getRealSize()

        vxPos = (vPos[0] / aOldWidth) * aNewWidth
        vyPos = (vPos[1] / aOldHeight) * aNewHeight

        self.mSize = (vSize[0] / aOldWidth) * aNewWidth
        vFontSize = (self.mButtons[0].getFontSize() / aOldWidth) * aNewWidth

        for y in range(len(self.mButtonMap)):
            for x in range(len(self.mButtonMap[y])):
                self.mButtonMap[x][y].setLocation(vxPos + x*(self.mSize+self.mBuffer), vyPos + y*(self.mSize+self.mBuffer))
                self.mButtonMap[x][y].setSize(self.mSize, self.mSize)
                self.mButtonMap[x][y].setFontSize(vFontSize)


    # interactivity
    def mouseDown( self, aMousePos ):
        for button in self.mButtons:
            button.mouseDown(aMousePos)

    def mouseUp( self, aMousePos):
        for button in self.mButtons:
            button.mouseUp(aMousePos)

    def keyDown( self, aKey ):

        vx = 0
        vy = 0

        if aKey == pg.K_w:
            vy = Settings.CAMERASPEED*2
        elif aKey == pg.K_s:
            vy = -Settings.CAMERASPEED*2
        elif aKey == pg.K_a:
            vx = Settings.CAMERASPEED*2
        elif aKey == pg.K_d:
            vx = -Settings.CAMERASPEED*2

        # updating all of the tiles' locations is lags too much
        for y in range(len(self.mButtonMap)):
            for x in range(len(self.mButtonMap[y])):
                vPos = self.mButtonMap[x][y].getLocation()
                self.mButtonMap[x][y].setLocation(vPos[0]+vx, vPos[1]+vy)

    def keyUp( self, aKey ):
        pass

    # getters and setters
    def getTiles( self ):
        return self.mTiles