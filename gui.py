# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

# interface for controlling all of the gui components

import pygame as pg
from menu import Menu, Position
from settings import Settings, GameState
from mapeditor import Editor
from component import *
from button import *
from label import *

class GUI():

    def __init__( self ):
        # array of menus
        self.mMenus = []
        self.mMenuInView = None

    # menu function wrappers
    def drawAll( self, aScreen ):
        if self.mMenuInView:
            self.mMenuInView.drawAll(aScreen)

    # event handling
    def mouseDown(self, aMousePos):
        if self.mMenuInView:
            self.mMenuInView.mouseDown(aMousePos)

    def mouseUp(self, aMousePos):
        if self.mMenuInView:
            self.mMenuInView.mouseUp(aMousePos)

    def resizeComponents( self, aOldWidth, aOldHeight, aNewWidth, aNewHeight ):
        for menu in self.mMenus:
            menu.resizeComponents(aOldWidth, aOldHeight, aNewWidth, aNewHeight)

    def keyDown( self, aKey ):
        if self.mMenuInView:
            self.mMenuInView.keyDown(aKey)

    def keyUp( self, aKey ):
        if self.mMenuInView:
            self.mMenuInView.keyUp(aKey)

    # menu wrappers
    def startMenu( self, aGame ):
        aGame.mGameState = GameState.MAINMENU
        self.mStartMenu = Menu()
        self.mStartMenu.setPositioning(5, Settings.WIDTH / 3.2, Settings.HEIGHT / 10, Position.CENTER, Position.CENTER)
        self.mStartMenu.addLabel(Settings.TITLE, 0)
        self.mStartMenu.addButton("Start Game", lambda: None, 1)
        self.mStartMenu.addButton( 'Continue', lambda: self.loadMenu(aGame), 2 )
        self.mStartMenu.addButton("Map Editor", lambda: self.editorMenu(aGame), 3)
        self.mStartMenu.addButton("Options", lambda: print("We have no options yet"), 4)
        self.mStartMenu.addButton("Quit", lambda: aGame.quit(), 5)
        self.mStartMenu.setVisibleToggle(False)
        self.mMenus.append(self.mStartMenu)
        self.mMenuInView = self.mStartMenu

    def endStartMenu( self, aGame ):
        del self.mStartMenu
        self.mMenuInView = None
        self.mMenus = []

    ########################
    def loadMenu( self, aGame ):
        self.mLoadMenu = Menu()
        self.mLoadMenu.setPositioning(4, Settings.WIDTH / 3.2, Settings.HEIGHT / 10, Position.CENTER, Position.CENTER)
        self.mLoadMenu.addLabel( "Select Savegame to Load: ", 0 )
        self.mLoadMenu.addButton( "Slot 1", lambda self = self, aGame = aGame, aSlot = saveGames.SaveGame1 : self.loadGameFromLoadMenu( aGame, aSlot ), 1 )
        self.mLoadMenu.addButton( "Slot 2", lambda self = self, aGame = aGame, aSlot = saveGames.SaveGame2 : self.loadGameFromLoadMenu( aGame, aSlot ), 2 )
        self.mLoadMenu.addButton( "Autosave Slot", lambda self = self, aGame = aGame, aSlot = saveGames.AutoSave : self.loadGameFromLoadMenu( aGame, aSlot ), 3 )
        self.mLoadMenu.addButton( "Back", lambda : self.backOnLoadMenu(), 4 )
        self.mLoadMenu.setVisibleToggle( False )
        self.mMenus.append( self.mLoadMenu )
        self.mMenuInView = self.mLoadMenu

    def backOnLoadMenu( self ):
        self.mMenus.remove( self.mLoadMenu )
        del self.mLoadMenu
        self.mMenuInView = self.mStartMenu

    def endLoadMenu( self ):
        self.mMenus.remove( self.mLoadMenu )
        del self.mLoadMenu

    def loadGameFromLoadMenu( self, aGame, aSlot ):
        vRetVal = aGame.loadGame( aSlot )
        if vRetVal < 0:
            # fail condition
            return
        else:
            self.endLoadMenu()
            self.endStartMenu( aGame )

    def editorMenu( self, aGame ):
        self.mEditorMenu = Menu()
        self.mEditorMenu.setPositioning(4, Settings.WIDTH / 3.2, Settings.HEIGHT / 10, Position.CENTER, Position.CENTER)
        self.mEditorMenu.addLabel("Map Editor", 0)
        self.mEditorMenu.addButton("Create Map", lambda: self.editorCreateMenu(aGame), 1)
        self.mEditorMenu.addButton("Load Map", lambda: self.editorLoadMenu(aGame), 2)
        self.mEditorMenu.addButton("Back", lambda: self.endEditorMenu(), 3)
        self.mEditorMenu.setVisibleToggle(False)
        self.mMenus.append(self.mEditorMenu)
        self.mMenuInView = self.mEditorMenu

    def endEditorMenu( self ):
        self.mMenus.remove(self.mEditorMenu)
        del self.mEditorMenu
        self.mMenuInView = self.mStartMenu

    def editorCreateMenu( self, aGame ):
        self.mEditorCreateMenu = Menu()
        self.mEditorCreateMenu.setPositioning(4, Settings.WIDTH / 3.2, Settings.HEIGHT / 10, Position.CENTER, Position.CENTER)
        self.mEditorCreateMenu.addLabel("Create a New Map", 0)
        self.mEditorCreateMenu.addButton("Create", lambda: self.startEditor(aGame), 3)
        self.mEditorCreateMenu.addButton("Back", lambda: self.endEditorCreateMenu(), 4)

        #create custom components and store them in position two
        vWidth = self.mEditorCreateMenu.getComponentWidth() / 3
        vHeight = self.mEditorCreateMenu.getComponentHeight()
        vXPos = self.mEditorCreateMenu.getComponentXPos()
        vYPos = self.mEditorCreateMenu.getComponentYPos() + vHeight*2
        vPadding = self.mEditorCreateMenu.getComponentPadding()

        self.mWidthTextfield = Label(vXPos - vPadding, vYPos, vWidth, vHeight, "Width")
        self.mByTextfield = Label(vXPos + vWidth, vYPos, vWidth, vHeight, "by")
        self.mHeightTextfield = Label(vXPos + vWidth*2 + + vPadding, vYPos, vWidth, vHeight, "Height")
        self.mEditorCreateMenu.addComponents([self.mWidthTextfield, self.mByTextfield, self.mHeightTextfield])

        self.mMenus.append(self.mEditorCreateMenu)
        self.mMenuInView = self.mEditorCreateMenu

    def endEditorCreateMenu( self ):
        self.mMenus.remove(self.mEditorCreateMenu)
        del self.mEditorCreateMenu
        self.mMenuInView = self.mEditorMenu

    def editorLoadMenu( self, aGame ):
        self.mEditorLoadMenu = Menu()
        self.mEditorLoadMenu.setPositioning(5, Settings.WIDTH / 3.2, Settings.HEIGHT / 10, Position.CENTER, Position.CENTER)
        self.mEditorLoadMenu.addLabel("Load an Existing Map", 0)
        self.mEditorLoadMenu.addButton("Browse for a file", lambda: print("You browsed for a file!"), 2)
        self.mEditorLoadMenu.addButton("Load", lambda: self.startEditor(aGame), 3)
        self.mEditorLoadMenu.addButton("Back", lambda: self.endEditorLoadMenu(), 4)
        self.mMenus.append(self.mEditorLoadMenu)
        self.mMenuInView = self.mEditorLoadMenu

    def endEditorLoadMenu( self ):
        self.mMenus.remove(self.mEditorLoadMenu)
        del self.mEditorLoadMenu
        self.mMenuInView = self.mEditorMenu

    def startEditor( self, aGame ):
        aGame.mGameState = GameState.EDITOR
        self.mEditor = Editor()
        self.mEditor.startEditor(aGame, self)

        self.mMenus.append(self.mEditor.getMenu())
        self.mMenuInView = self.mEditor.getMenu()

    def endEditor( self, aGame ):
        aGame.mGameState = GameState.MAINMENU
        self.mMenus.remove(self.mEditor.getMenu())
        self.mEditor.endEditor()
        del self.mEditor

        # remove any sub menus existing menus
        for menu in self.mMenus:
            if menu is self.mStartMenu:
                continue
            else:
                self.mMenus.remove(menu)
                del menu

        self.mMenuInView  = self.mStartMenu

    # menus to be implemented
    def optionsMenu( self, aGame ):
        raise NotImplementedError("This is has not been implemented.")

    def endOptionsMenu( self, aGame ):
        raise NotImplementedError("This is has not been implemented.")

    def gameoverMenu( self, aGame ):
        raise NotImplementedError("This is has not been implemented.")

    def endGameoverMenu( self, aGame ):
        raise NotImplementedError("This is has not been implemented.")

    def addCityMenu( self ):
        raise NotImplementedError("This is has not been implemented.")