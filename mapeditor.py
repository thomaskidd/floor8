# class for user friendly map editor

from menu import Menu, Position
from settings import Settings
from component import *
from button import *
from label import *
from tileEditor import TileEditor, TileType

class Editor():

    def __init__( self ):
        self.mCurrentMap = []
        self.mMenu = Menu()

    # gui component initalizers and destructors
    def startEditor( self, aGame, aGUI ):
        self.mMenu.setPositioning(10, Settings.WIDTH / 8, Settings.HEIGHT / 15, Position.LEFT, Position.CENTER)
        self.mMenu.addLabel("Tiles", 0)
        self.mMenu.addButton("Grass Tile", lambda: self.setSelectedTileType(TileType.GRASS), 2)
        self.mMenu.addButton("Forest Tile", lambda: self.setSelectedTileType(TileType.FOREST), 3)
        self.mMenu.addButton("Water Tile", lambda: self.setSelectedTileType(TileType.WATER), 4)
        self.mMenu.addButton("Plain Tile", lambda: self.setSelectedTileType(TileType.PLAIN), 5)
        self.mMenu.addButton("City Tile", lambda: self.setSelectedTileType(TileType.CITY), 6)
        self.mMenu.addButton("Save", lambda: aGUI.endEditor(aGame), 8)
        self.mMenu.addButton("Exit", lambda: aGUI.endEditor(aGame), 9)

        # create tileEditor object - this has a similar interface to a menu
        self.mTileEditor = TileEditor(self, Settings.WIDTH / 6, Settings.HEIGHT / 10, 10, 10)

        # add the tile Editor to self.mMenu
        self.mMenu.addContainer(self.mTileEditor)

        # for tile selection
        self.mSelectedTileType = TileType.GRASS

    def endEditor( self ):
        # save the map
        del self.mMenu

    def getMenu( self ):
        return self.mMenu

    # tile getting and setting functions
    def setSelectedTileType( self, aTileType ):
        self.mSelectedTileType = aTileType

    def getSelectedTileType( self ):
        return self.mSelectedTileType


    # saving and loading functions
    def loadMap( self, map ):
        raise NotImplementedError("This has not been implemented.")

    def saveMap( self ):
        raise NotImplementedError("This has not been implemented.")

    def validateMap( self ):
        vValidSave = True

        for row in self.mCurrentMap:
            for tile in row:
                if tile == "":
                    vValidSave = False
                    # set the tile to something obvious - like a red square

        return vValidSave
