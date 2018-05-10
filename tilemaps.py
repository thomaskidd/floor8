import pygame as pg
from settings import *
from spritesList import *
from keybindings import *
from eventHandling import *
from mapDicts import *
import sprites
import player
import unitSprites

class Camera():
    def __init__( self, aGame, aPosX, aPosY ):
        self.mGame = aGame
        self.xShift = 0
        self.yShift = 0
        self.xDisplacement = 0
        self.yDisplacement = 0
        self.vX = 0
        self.vY = 0
        self.mZoomFactor = 1.
        self.mZoomChange = 1.

    def apply( self, aObjectRect, aObject = None ):
        self.applyZoom( aObject )
        vRv = aObjectRect.move( self.xShift, self.yShift)
        return vRv

    def applyZoom( self, aObject ):
        if aObject:
            vWidth = self.mGame.mCurrentTileSize
            vHeight = self.mGame.mCurrentTileSize
            aObject.image = pg.transform.scale( aObject.mOrigImage, (vWidth, vHeight) )
            # aObject.rect = aObject.image.get_rect()
            aObject.rect.x = (aObject.x * self.mGame.mCurrentTileSize)
            aObject.rect.y = (aObject.y * self.mGame.mCurrentTileSize)
            aObject.rect.width = vWidth
            aObject.rect.height = vHeight

    def applyShift( self ):
        vDeltaXFromScreen, vDeltaYFromScreen = pg.mouse.get_pos()

        vMouseXRelativePos = vDeltaXFromScreen - self.xShift
        vMouseYRelativePos = vDeltaYFromScreen - self.yShift

        self.xShift += -((self.mZoomChange - 1) * vMouseXRelativePos)
        self.yShift += -((self.mZoomChange - 1) * vMouseYRelativePos)

        if self.mGame.mVerbosity == 5:
            print('\nZoomFactor: ', self.mZoomFactor)
            print('ZoomChange: ', self.mZoomChange)
            print('MousePos: ', vDeltaXFromScreen/self.mGame.mCurrentTileSize, ' , ', vDeltaYFromScreen/self.mGame.mCurrentTileSize)
            print('ShiftedPos: ', vMouseXRelativePos/self.mGame.mCurrentTileSize, ' , ', vMouseYRelativePos/self.mGame.mCurrentTileSize)
            print('Shift: ', self.xShift/self.mGame.mCurrentTileSize, ' , ', self.yShift/self.mGame.mCurrentTileSize)
        elif self.mGame.mVerbosity >= 6:
            print('\nZoomFactor: ', self.mZoomFactor)
            print('ZoomChange: ', self.mZoomChange)
            print('MousePos: ', vDeltaXFromScreen, ' , ', vDeltaYFromScreen)
            print('ShiftedPos: ', vMouseXRelativePos, ' , ', vMouseYRelativePos)
            print('Shift: ', self.xShift, ' , ', self.yShift)

    def getSpeed( self ):
        self.vX = 0
        self.vY = 0
        vPressedKeys = pg.key.get_pressed()
        if vPressedKeys[pg.K_a]:
            self.vX = Settings.CAMERASPEED
        if vPressedKeys[pg.K_d]:
            self.vX = -Settings.CAMERASPEED
        if vPressedKeys[pg.K_w]:
            self.vY = Settings.CAMERASPEED
        if vPressedKeys[pg.K_s]:
            self.vY = -Settings.CAMERASPEED
        if self.vX != 0 and self.vY != 0:
            self.vX *= 0.7071
            self.vY *= 0.7071
        self.vX *= int( self.mZoomFactor ** Settings.ZOOMCAMERASPEEDEXPONENT )
        self.vY *= int( self.mZoomFactor ** Settings.ZOOMCAMERASPEEDEXPONENT )

    def update( self ):
        self.getSpeed()
        self.xShift += self.vX
        self.yShift += self.vY

        # border collision code
        # math to calculate the far edge
        vFarXEdge = -((self.mGame.mCurrentTileSize * self.mGame.mMap.mapWidth) + Settings.BORDERWIDTH) + Settings.WIDTH
        # the signs need to change depending on how big the screen is
        if vFarXEdge - Settings.BORDERWIDTH > 0:
            if self.xShift > vFarXEdge:
                self.xShift = vFarXEdge

            elif self.xShift < Settings.BORDERWIDTH:
                self.xShift = Settings.BORDERWIDTH

        else:
            if self.xShift < vFarXEdge:
                self.xShift = vFarXEdge

            elif self.xShift > Settings.BORDERWIDTH:
                self.xShift = Settings.BORDERWIDTH

        vFarYEdge = -((self.mGame.mCurrentTileSize * self.mGame.mMap.mapHeight) + Settings.BORDERWIDTH) + Settings.HEIGHT
        if vFarYEdge - Settings.BORDERWIDTH > 0:
            if self.yShift < vFarYEdge:
                self.yShift = vFarYEdge

            elif self.yShift > Settings.BORDERWIDTH:
                self.yShift = Settings.BORDERWIDTH

        else:
            if self.yShift < vFarYEdge:
                self.yShift = vFarYEdge

            elif self.yShift > Settings.BORDERWIDTH:
                self.yShift = Settings.BORDERWIDTH
class Map:
    def __init__(self, aGame):
        self.mGame = aGame

    def update(self):
        pass


class TerrainMap(Map):
    def __init__(self, aGame, aMapData, aStartingPlayer, aUnitInfoList, aPlayerInfoList, aCityInfo ):
        # when creating a new map, clear the old player objects so new ones can be instantiated
        aGame.mPlayers.clear()

        self.mGame = aGame
        self.mapHeight = 0
        self.mapWidth = 0
        self.mMapData = []
        self.mTileDict = {}
        vY = 0

        self.mGame.mSelector = sprites.Selector( self.mGame )
        self.mGame.mSelected = sprites.Selected( self.mGame )

        aGame.mCurrentPlayerTurn = aStartingPlayer

        # add the player obj to the current players dictionary
        for vPlayer in aPlayerInfoList:
            vPlayerId = vPlayer[0]
            vPlayerMoney = vPlayer[1]
            vPlayerObj = player.Player( self.mGame, vPlayerId, vPlayerMoney )
            aGame.mPlayers[vPlayerId] = vPlayerObj

        aGame.mNumPlayers = int( len( aPlayerInfoList ) )

        # have to open the file twice as we run through it twice
        for vRow in aMapData :
            for vTile in vRow :
                if self.mapWidth < len( vRow ):
                    self.mapWidth = len( vRow )
            self.mapHeight += 1

        if aGame.mVerbosity >= 1:
            print('Mapsize: ', self.mapWidth, 'x', self.mapHeight)
        for vRow in aMapData:
            vMapRowData = []
            vX = 0
            for vTileChar in vRow:
                if len( vRow ) > 0 :
                    import tileDict
                    vTileConstructor = tileDict.tileDict[vTileChar]
                    if vTileChar in 'zxcvb':
                        try:
                            vCityOwner = aCityInfo[(vX, vY)]
                        except:
                            vCityOwner = None
                        vTile = self.createTile( vTileConstructor, vX, vY, vCityOwner )
                    else:
                        vTile = self.createTile( vTileConstructor, vX, vY )

                    vMapRowData.append( vTileChar )
                    self.mTileDict[ ( vX, vY ) ] = vTile
                    vX += 1
            self.mMapData.append( vMapRowData )
            vY += 1

        for vUnit in aUnitInfoList:
            # unit info : ( self.mName, ( self.x, self.y ), self.mPlayerId, self.mHealth, self.mLevel )
            vUnitName = vUnit[0]
            vUnitXPos = vUnit[1][0]
            vUnitYPos = vUnit[1][1]
            vPlayerId = vUnit[2]
            vUnitHealth = vUnit[3]
            vUnitLevel = vUnit[4]
            vUnitConstructor = getattr( sprites, vUnitName )
            vTile = self.mTileDict[(vUnitXPos, vUnitYPos)]
            vUnitConstructor( self.mGame, vTile, vPlayerId, vUnitHealth, vUnitLevel )
            if aGame.mVerbosity >= 5:
                print('Units being constructed', vUnitName)

        if aGame.mVerbosity >= 2:
            print('vnumplayers', aGame.mNumPlayers)

        # leave these for debug

        # unitSprites.LightInfantry(self.mGame, self.mTileDict[ ( 13, 10 ) ], 0, 98, 1)
        # unitSprites.LightInfantry( self.mGame, self.mTileDict[(13, 12)], 1, 27, 1 )
        # unitSprites.LightInfantry( self.mGame, self.mTileDict[(10, 14)], 0, 76, 1 )
        # unitSprites.LightInfantry( self.mGame, self.mTileDict[(10, 16)], 1, 100, 1 )
        # unitSprites.Battleship( self.mGame, self.mTileDict[(5, 5)], 0, 100, 1 )
        # unitSprites.Battleship( self.mGame, self.mTileDict[(5, 2)], 1, 100, 1 )

        #assuming all is well and generated, create the camera obj
        self.mXCenter = ( self.mapWidth * Settings.TILESIZE ) / 2
        self.mYCenter = ( self.mapHeight * Settings.TILESIZE ) / 2
        # TODO currently the centers dont acutlaly do anything, yes I spelled that wrong thanks Andrew
        self.mGame.mCamera = Camera( self.mGame, self.mXCenter, self.mYCenter )

        # after everything has finished, change game state last to avoid bugs
        self.mGame.mGameState = GameState.HUMANPLAYER

    def closeMap( self ):
        for vSpriteGroup in self.mGame.mAllSpriteGroups:
            vSpriteGroup.empty()
        # TODO, we need to delete all sprites, including selector/selected, all units, all tiles and players
        # TODO, this should maybe be something different
        # self.mGUI.startMenu( self )

    def update(self):
        pass

    def createTile( self, aConstructor, aXPos, aYPos, aOwner = 'notpassed' ):
        # aOwner can be 0 or None or it can maybe not be passed
        # which means it needs a default value, however that default can not be None or 0, since those are valid passing values
        # this string is good enough
        # do not change this without asking dennyv
        if aOwner == 'notpassed':
            vRv = aConstructor( self.mGame, aXPos, aYPos )
        else:
            vRv = aConstructor( self.mGame, aXPos, aYPos, aOwner )
        return vRv
