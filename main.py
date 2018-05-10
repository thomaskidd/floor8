# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

import pygame as pg
from settings import *
from sprites import *
from terrainSprites import *
from unitSprites import *
from spritesList import *
from eventHandling import *
from tilemaps import *
import cursur
from gui import *
import os
import sys
import pickle

os.environ['SDL_VIDEO_WINDOW_POS'] = '100, 100'



class Game:
    def __init__( self ):
        pg.init()
        # This variable is for debugging.
        self.mVerbosity = gVerbosity
        self.Settings = Settings()
        self.screenRegionSetup()
        pg.display.set_caption( self.Settings.TITLE )
        self.mClock = pg.time.Clock()

        #initialize GUI
        self.mGUI = GUI()

        # Allows a key to be pushed down and behave naturally
        pg.key.set_repeat( Settings.KEY_INPUT_DELAY, Settings.KEY_INPUT_INPUT_INTERVAL )

    def startMenu( self ):
        self.mGUI.startMenu(self)

    def endStartMenu( self ):
        self.mGUI.endStartMenu(self)
        # self.mGUI.startOptionsMenu(self)

        # TODO ///////////////////////////////////////////
        self.loadGame()
        # self.makeMap('testmap1', 2, [])
        # TODO// Map init should definetly not be here
        # TODO// however since it's only for testing it's fine
        # TODO create a wrapper for loading maps

    def setup( self ):
        # initialize variables and setup for a new game
        self.mAllSpritesGroup = pg.sprite.Group()
        self.mAllTerrainGroup = pg.sprite.Group()
        self.mAllSelectorsGroup = pg.sprite.Group()
        self.mAllUnitsGroup = pg.sprite.Group()
        self.mAllPathingGroup = pg.sprite.Group()
        self.mAllPathDisplayGroup = pg.sprite.Group()
        self.mAllHealthBarsGroup = pg.sprite.Group()
        self.mAllTargetGroup = pg.sprite.Group()
        self.mCameraGroup = pg.sprite.Group()
        self.mAllCameraCollideGroup = pg.sprite.Group()
        self.mAllSpriteGroups = [
            self.mAllSpritesGroup,
            self.mAllTerrainGroup,
            self.mAllSelectorsGroup,
            self.mAllUnitsGroup,
            self.mAllPathingGroup,
            self.mAllPathDisplayGroup,
            self.mAllHealthBarsGroup,
            self.mAllTargetGroup,
            self.mCameraGroup,
            self.mAllCameraCollideGroup,
        ]

        # move animations
        self.mShortestPathList = None
        # self.mUnitMoving = None

        self.mCamera = None # initialize as none, create when on a map
        self.mGameState = GameState.MAINMENU
        self.mCurrentPlayerTurn = None
        self.mNumPlayers = None
        self.mCurrentTileSize = Settings.TILESIZE

        self.mPrevMouseXRelativePos = 0
        self.mPrevMouseYRelativePos = 0
        self.mZoomChanged = 0

        # this is a dict of player objects.
        # the key should alwways be the player ID ( 0, 1, 2, 3 )
        self.mPlayers = {}

        # this variable allows the console to skip a frame after a command is inputed,
        # which means you can actually see your changes happen
        self.inConsoleSkipFrame = False
		
        pg.font.init()
        cursur.createCursorFromStrings()

        self.mSelector = None
        self.mSelected = None

    def makeMap( self, aMapName, aNumPlayers ):
        self.mMap = TerrainMap( self, 'testmap1', 0 )
        self.mGameState = GameState.HUMANPLAYER

    def screenRegionSetup( self ):
        startUpScreenRes = pg.display.list_modes()[9] # TODO REPLACE HARDCODED VALUES
        self.screenRegionConfig( startUpScreenRes, self.Settings.DEFAULT_DISPLAY_SETTING )

    #this functions changes the screen size and aFullscreen
    # args: aDimensions is a tuple of ( WIDTH, HEIGHT )
    # aFullscreen should be from the FullscreenSettings class
    # 0 = windowed, 1 = fullscreen, 2 = borderless windowed
    def screenRegionConfig( self, aDimensions, aScreenDisplayType ):
        if aScreenDisplayType == FullscreenSettings.FULLSCREEN:
            maxScreenRes = pg.display.list_modes()[0] # TODO replace with a menu select later
            self.mScreen = pg.display.set_mode( maxScreenRes, pg.FULLSCREEN )

        elif aScreenDisplayType == FullscreenSettings.BORDERLESS_WINDOW:
            self.mScreen = pg.display.set_mode(aDimensions, pg.RESIZABLE)

        elif aScreenDisplayType == FullscreenSettings.WINDOWED:
            self.mScreen = pg.display.set_mode( aDimensions, pg.RESIZABLE )
        else:
            print( 'Argument error (%i), unsupported aScreenDisplayType' % aScreenDisplayType)

        #update width and height setting!
        self.Settings.setWidth( aDimensions[0] )
        self.Settings.setHeight( aDimensions[1] )

    def runGame( self ):
        """
        Game main loop, change mInGame to exit
        :return:
        """
        # start menu
        self.startMenu()

        # game loop
        # set self.mInGame to false to exit game loop
        self.mInGame = True
        while self.mInGame:
            self.mDeltaTime = self.mClock.tick( self.Settings.FPS )
            eventHandling(self)
            self.updateAll()
            self.drawAll()

        self.quit()

    def cleanUpPathingTiles( self ) :
        for vSprite in self.mAllPathingGroup :
            vSprite.mTile.mInPathing = False
            vSprite.kill()

    def cleanUpPathDisplayTiles (self):
        for vSprite in self.mAllPathDisplayGroup:
            vSprite.kill()
        for vSprite in self.mAllPathingGroup:
            vSprite.mTile.mPathParent = None

    def cleanUpTargetTiles( self ):
        for vSprite in self.mAllTargetGroup:
            if vSprite.mTile.mUnit != None:
                vSprite.mTile.mUnit.mIsTargetted = False
                vSprite.mTile.mUnit.mIsTargettedOutOfRange = False
            vSprite.kill()

    def skipAnimations( self ):
        for vUnit in self.mAllUnitsGroup:
            if vUnit.mIsDead:
                vUnit.killUnit()
            vUnit.mAnimationQueue.clear()
            vUnit.mBlockerGroup.clear()
            vUnit.mAnimationState = vUnit.mAnimationQueue.updateAction()
            vUnit.updatePos()
            vUnit.mHealthBar.updateHealthBar()


    def nextTurn( self ):
        # is this the last player
        if self.mCurrentPlayerTurn == ( self.mNumPlayers - 1 ):
            # if yes, return to first player's turn
            self.mCurrentPlayerTurn = 0
        else:
            # else, move to next player
            self.mCurrentPlayerTurn += 1

        vCurrentPlayerObj = self.mPlayers[self.mCurrentPlayerTurn]
        for vCity in vCurrentPlayerObj.mCitiesOwned:
            #TODO make cities unique rather than aflat bonus
            vCurrentPlayerObj.mMoney += 100

        if self.mVerbosity >= 1:
            print( vCurrentPlayerObj.mMoney )
            print( 'Num players: ', self.mNumPlayers )
            print('Current player: ', self.mCurrentPlayerTurn )

        self.skipAnimations()

        if self.mSelected.mTile != None:
            self.mSelected.mTile.deselect()

        for vUnit in vCurrentPlayerObj.mUnits:
            vUnit.mMovesLeft = vUnit.mRange
            vUnit.mNumberOfAttacks = 1


    def drawGrid( self ):
        for vX in range( 0, self.Settings.WIDTH, self.Settings.TILESIZE ):
            pg.draw.line( self.mScreen, self.Settings.BLACK, ( vX, 0 ), ( vX, self.Settings.HEIGHT ) )
        for vY in range( 0, self.Settings.HEIGHT, self.Settings.TILESIZE ):
            pg.draw.line( self.mScreen, self.Settings.BLACK, ( 0, vY ), ( self.Settings.WIDTH, vY ) )

    def updateAll( self ):
        if self.mGameState != GameState.MAINMENU:
            # update all sprites
            self.mAllSpritesGroup.update()
        if self.mCamera:
            self.mCamera.update()

    def drawAll( self ):
        # the order of this has to be very specific
        # things called first will be painted over

        if self.mVerbosity == 10 and self.mCamera != None:
            vDeltaXFromScreen, vDeltaYFromScreen = pg.mouse.get_pos()
            vMouseXRelativePos = vDeltaXFromScreen - self.mCamera.xShift
            vMouseYRelativePos = vDeltaYFromScreen - self.mCamera.yShift 
            print('ShiftedPos: ', vMouseXRelativePos, ' , ', vMouseYRelativePos)

        self.mScreen.fill( self.Settings.BGCOLOR )
        if self.mCamera:
            self.mDifBetweenTiles = int( Settings.TILESIZE * self.mCamera.mZoomFactor ) - self.mCurrentTileSize
            self.mCurrentTileSize = int( Settings.TILESIZE * self.mCamera.mZoomFactor )
        if self.mCamera and self.mGameState != GameState.MAINMENU:
            vSpriteGroup = [
                self.mAllTerrainGroup,      self.mAllSelectorsGroup,
                self.mAllPathingGroup,      self.mAllUnitsGroup,
                self.mAllTargetGroup,       self.mAllHealthBarsGroup,
                self.mAllPathDisplayGroup,
                ]

            if self.mZoomChanged:
                self.mCamera.applyShift()
                self.mZoomChanged = 0

            for vGroup in vSpriteGroup:
                for vSprite in vGroup:
                    vRect = self.mCamera.apply(vSprite.rect, vSprite) 
                    self.mScreen.blit( vSprite.image, vRect )

        # this handles the drawing of all GUI components
        self.mGUI.drawAll(self.mScreen)
        pg.display.flip()

    def saveGame( self, aFile, aExit = None ):
        # aExit is an optional arg to provide if you want to save and exit

        # TODO come up with a better name for the outfile, ideally should be chooseable?
        # TODO or maybe you just have 3 slots to save to
        vFile = gSaveGameDict[ aFile ]
        pickleOutFile = open( vFile, 'wb' )
        pickle.dump( ( self.mMap.mMapData, self.mCurrentPlayerTurn), pickleOutFile )
        vUnitList = []
        for vSprite in self.mAllUnitsGroup:
            vUnitInfo = vSprite.saveHelper()
            vUnitList.append( vUnitInfo )
        pickle.dump( vUnitList, pickleOutFile )
        vPlayerList = []
        for vKey in self.mPlayers.keys():
            vPlayerObj = self.mPlayers[vKey]
            vPlayerInfo = vPlayerObj.saveHelper()
            vPlayerList.append( vPlayerInfo )
        pickle.dump( vPlayerList, pickleOutFile )

        vCityDict = {}
        for vTile in self.mAllTerrainGroup:
            if vTile.mType in [TerrainTypes.cityTile, TerrainTypes.blueCityTile, TerrainTypes.redCityTile]:
                vCityDict[( vTile.x, vTile.y )] = vTile.mPlayerId
        pickle.dump( vCityDict, pickleOutFile )
        if aExit:
            self.exitMap()
        pickleOutFile.close()

    def loadGame( self, aFile = saveGames.AutoSave ):
        """
        Loads a game from the selected game slot
        :param aFile: value from saveGames enum
        :return: 0 on success, <0 on fail
        """
        vRv = 0
        #TODO change the filename

        #TODO call the exit game function (DNE currently) first?

        #if loading from in game, delete current game before attempting a reload
        #TODO prompt save first?
        if self.mGameState in INGAMESTATES:
            self.exitMap()

        vFilename = gSaveGameDict[aFile]
        try:
            vLoaded = list(self.loadAllFromPickle( vFilename ))
        except FileNotFoundError:
            print("Nothing saved to this slot!")
            vRv = -1
            return vRv
        vMapInfo = vLoaded[0]
        # tilemap lists
        vMapTileLayout = vMapInfo[0]

        # int value of first player
        vFirstPlayer = vMapInfo[1]

        # list of units ( self.mName, ( self.x, self.y ), self.mPlayerId, self.mHealth, self.mLevel )
        vUnitInfo = vLoaded[1]

        # list of players ( self.mID, self.mMoney )
        vPlayerInfo = vLoaded[2]

        # city dict: (x,y):owner
        vCityInfo = vLoaded[3]

        #TODO move this to function
        self.mMap = TerrainMap( self, vMapTileLayout, vFirstPlayer, vUnitInfo, vPlayerInfo, vCityInfo )
        return vRv

    def loadAllFromPickle( self, aFilename ) :
        with open( aFilename, "rb" ) as vFile:
            while True:
                try:
                    yield pickle.load( vFile )
                except EOFError:
                    break

    def exitMap( self ):
        self.mMap.closeMap()

    def quit( self, aSave = 0 ):
        # save game before exit
        if aSave:
            vExit = aSave
            self.saveGame( saveGames.AutoSave, aExit = vExit )
        pg.display.quit()
        pg.quit()
        sys.exit()

if __name__ == '__main__':
    vArgs = sys.argv
    if len( vArgs ) > 2:
        raise Exception( """
Too many command line arguments!
Currently we support only 1, for verbosity
""" )
    global gVerbosity
    try:
        gVerbosity = vArgs[1]
    except IndexError:
        gVerbosity = 0

    try:
        gVerbosity = int( gVerbosity )
    except ValueError:
        print('Verbosity must be given as integer!')
    # create the game object
    gameObj = Game()
    while True:
        gameObj.setup()
        gameObj.runGame()
