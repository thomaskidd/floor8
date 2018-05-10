import pygame as pg
from settings import *
from spritesList import *
from keybindings import *
from terrainSprites import *
from unitSprites import *

class Selector( pg.sprite.Sprite ):
    def __init__( self, aGame ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllSelectorsGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.image = spritesImageDict['selectorIcon']
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.x = 300
        self.y = 300
        self.mFoundTile = False
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mTile = None

    def update( self ):
        if self.mGame.mCamera:
            self.mFoundTile = False
            (vMouseX, vMouseY) = pg.mouse.get_pos()
            vDisplacedX = vMouseX - self.mGame.mCamera.xShift
            vDisplacedY = vMouseY - self.mGame.mCamera.yShift
            for vTile in self.mGame.mAllTerrainGroup:
                if vTile.rect.collidepoint(vDisplacedX, vDisplacedY):
                    self.mFoundTile = True
                    self.mGame.mSelector.mTile = vTile
                    self.mGame.mSelector.moveSelector()
            # if no tile is found it means cursor is off the map
            if self.mFoundTile == False:
                self.mGame.mSelector.mTile = None
                self.mGame.mSelector.moveSelector()

    def moveSelector( self ):
        if self.mTile != None and self.mTile.mType != TerrainTypes.fogTile:
            vX = self.x
            vY = self.y
            self.x = self.mTile.x
            self.y = self.mTile.y

            #  Mouse hover events
            if vX != self.x or vY != self.y:
                self.mGame.cleanUpPathDisplayTiles()
                if self.mTile.mInPathing or \
                (self.mTile.mUnit != None and self.mTile.mUnit.mIsTargettedOutOfRange):
                    vUnit = self.mGame.mSelected.mTile.mUnit
                    vEndTile = self.mTile.findBestPath(self.mGame.mSelected.mTile, self.mTile)
                    vUnit.mChangeInMoves = vEndTile.mGCost
                    vParent = vEndTile
                    vPathList = [vParent]
                    while vParent != None :
                        vParent = vParent.mPathParent
                        vPathList.append( vParent )
                    self.mGame.mShortestPathList = vPathList

        else:
            self.x = 300
            self.y = 300
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE

class Selected( Selector ):
    def __init__( self, aGame ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllSelectorsGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.image = spritesImageDict['selectedIcon']
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.x = 300
        self.y = 300
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mTile = None

    def update( self ):
        pass

    def moveSelector( self ):
        pass

    def moveSelected( self, aTile ):
        # change is selected flags
        if self.mTile != None:
            self.mTile.mIsSelected = False
            if self.mTile.mUnit != None:
                self.mTile.mUnit.mIsSelected = False
        self.mTile = aTile
        # move sprite
        if self.mTile != None:
            self.mTile.mIsSelected = True
            if self.mTile.mUnit != None:
                self.mTile.mUnit.mIsSelected = True
            self.x = self.mTile.x
            self.y = self.mTile.y
        else:
            self.x = 300
            self.y = 300
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE

class PathingTile( pg.sprite.Sprite ):
    def __init__( self, aGame, aTile ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllPathingGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.image = spritesImageDict['pathingIcon']
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.mTile = aTile
        self.x = aTile.x
        self.y = aTile.y
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE

# the one that highlights the attack range, mainly for artillery units
class AttackTile( pg.sprite.Sprite ):
    def __init__( self, aGame, aTile ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllTargetGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.image = spritesImageDict['attackIcon']
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.mTile = aTile
        self.x = aTile.x
        self.y = aTile.y
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE

class TargettedTile( AttackTile ):
    def __init__( self, aGame, aTile ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllTargetGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.image = spritesImageDict['targettedIcon']
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.mTile = aTile
        self.x = aTile.x
        self.y = aTile.y
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE

class PathDisplayTile( pg.sprite.Sprite ):
    def __init__( self, aGame, aTile, aImageKey ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllPathDisplayGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.image = spritesImageDict[aImageKey]
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.mTile = aTile
        self.x = aTile.x
        self.y = aTile.y
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE