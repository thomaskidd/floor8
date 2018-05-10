import pygame as pg
from settings import *
from spritesList import *
from keybindings import *
from heapq import heappush, heappop
import player

class TerrrainTile( pg.sprite.Sprite ):
    def __init__( self ):
        # self.mGroups = aGame.mAllSpritesGroup
        pass

    # Yusef's nasty workaround for using a priority queue. Needs to be here.
    def __lt__(self, other):
        return False

    def eventHandle( self, aAction ):
        self.mGame.skipAnimations()
        if aAction == EventActions.Select:
            # if the new tile in question has a unit
            self.mGame.cleanUpPathDisplayTiles()
            
            vSelectedTile = self.mGame.mSelected.mTile
            vSelectedUnit = None
            # if the tile is empty (no unit), and there is a selected tile
            if vSelectedTile != None:
                vSelectedTile = self.mGame.mSelected.mTile
                vSelectedUnit = self.mGame.mSelected.mTile.mUnit

            if self.mUnit != None:
                # if that unit is on the players team, switch focus to that unit
                if self.mUnit.mPlayerId == self.mGame.mCurrentPlayerTurn:
                    self.mUnit.findAttackRange()
                    self.findTiles()
                    self.mGame.mSelected.moveSelected(self)

                # if that unit is not on the players team and targetted, attack
                # (don't have to check if there is a selected tile as it's implied if the unit is targetted)
                elif self.mUnit.mIsTargetted:
                    vSelectedUnit.attack(self.mUnit)
                    self.mGame.mSelected.moveSelected(None)

                # move and attack (only for melee)
                elif self.mUnit.mIsTargettedOutOfRange:
                    # move tile to tile before target
                    vTileToMoveTo = self.mGame.mShortestPathList[0]
                    if vSelectedTile.moveUnit(vTileToMoveTo):
                        vSelectedTile.deselect()
                    # create a blocker on self.mUnit's animation queue
                    vSelectedUnit.mBlockerGroup.createTrigger()
                    vSelectedUnit.mBlockerGroup.createBlocker(self.mUnit)
                    vSelectedUnit.attack(self.mUnit)

            # if the selected tile has a unit, try to move the unit to this tile
            elif vSelectedUnit != None and vSelectedUnit.mMovesLeft:
                # move unit passes through the tile to the unit, returning a boolean for success
                if vSelectedTile.moveUnit(self):
                    vSelectedTile.deselect()
                # no action if move unit fails

            # if not one of the earlier cases, just move to that tile
            else:
                self.mGame.mSelected.moveSelected(self)



        elif aAction == EventActions.Deselect and self.mGame.mSelected.mTile != None:
            self.mGame.mSelected.mTile.deselect()

    def deselect( self ):
        self.mGame.mSelected.mTile.mIsSelected = False
        if self.mGame.mSelected.mTile.mUnit != None:
            self.mGame.mSelected.mTile.mUnit.mIsSelected = False
            self.mGame.cleanUpPathingTiles()
            self.mGame.cleanUpTargetTiles()
        self.mGame.mSelected.moveSelected(None)
        self.mGame.cleanUpPathDisplayTiles()

    def moveUnit ( self, aTile ):
        ret = self.mUnit.moveToTile(aTile)
        if ret == True:
            self.mUnit = None
            self.mIsAvailable = True
        return ret

    def findTiles( self ):
        self.mGame.cleanUpPathingTiles()
        self.findTilesRecur(self, self.mUnit, self.mUnit.mMovesLeft, None)

    def findTilesRecur( self, aTile, aUnit, aMovesRemaining, aParentTile ):
        import sprites
        vTileAdjacedent = []
        vTileAdjacedent.append(aTile.mGame.mMap.mTileDict.get( (aTile.x + 1, aTile.y), None ) )
        vTileAdjacedent.append(aTile.mGame.mMap.mTileDict.get( (aTile.x - 1, aTile.y), None ) )
        vTileAdjacedent.append(aTile.mGame.mMap.mTileDict.get( (aTile.x, aTile.y + 1), None ) )
        vTileAdjacedent.append(aTile.mGame.mMap.mTileDict.get( (aTile.x, aTile.y - 1), None ) )
        for vTile in vTileAdjacedent:
            if vTile != None and vTile != aParentTile:
                if aMovesRemaining > 0:
                    # if there is an enemy unit within range, target
                    if vTile.mIsAvailable == False:
                        if aUnit.allCheck(vTile.mUnit, vTile) and aUnit.mAttackType == AttackType.MELEE:
                            if not (vTile.mUnit.mIsTargetted or vTile.mUnit.mIsTargettedOutOfRange):
                                sprites.AttackTile(self.mGame, vTile)
                                sprites.TargettedTile(self.mGame, vTile)
                                vTile.mUnit.mIsTargettedOutOfRange = True
                    # otherwise if a viable tile, path it
                    elif aUnit.mTerrainDict[vTile.mType]:
                        if aMovesRemaining > 0:
                            if vTile.mInPathing == False:
                                sprites.PathingTile(aTile.mGame, vTile)
                                vTile.mInPathing = True
                            aTile.findTilesRecur(vTile, aUnit, aMovesRemaining - aUnit.mTerrainDict[vTile.mType], aTile)
                # look for units to attack at end of range    
                elif vTile.mIsAvailable == False and aUnit.mNumberOfAttacks > 0:
                    if aUnit.allCheck(vTile.mUnit, vTile) and aUnit.mAttackType == AttackType.MELEE:
                        if not (vTile.mUnit.mIsTargetted or vTile.mUnit.mIsTargettedOutOfRange):
                            sprites.AttackTile(self.mGame, vTile)
                            sprites.TargettedTile(self.mGame, vTile)
                            vTile.mUnit.mIsTargettedOutOfRange = True

    def findBestPath(self, aUnitStartTile, aEndTile):
        # this is a bool for when you move beside an enemy unit
        vFindOneBefore = False
        vUnit = aUnitStartTile.mUnit
        aUnitStartTile.mGCost = 0.
        vFrontier = []
        heappush(vFrontier , (0., aUnitStartTile))

        if aEndTile.mUnit != None and aEndTile.mUnit.mIsTargettedOutOfRange:
            vFindOneBefore = True

        while vFrontier.__len__() > 0:
            vCurrTile = heappop(vFrontier)[1]
            # gets neighboring tiles
            vTileAdjacedent = []
            vTileAdjacedent.append(vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x + 1, vCurrTile.y), None))
            vTileAdjacedent.append(vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x - 1, vCurrTile.y), None))
            vTileAdjacedent.append(vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x, vCurrTile.y + 1), None))
            vTileAdjacedent.append(vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x, vCurrTile.y - 1), None))

            # check neighboring tiles for validity and adds them to queue
            for vTile in vTileAdjacedent:
                if vTile is not None:
                    if vTile == aEndTile and vFindOneBefore:
                        vEndTile = self.makeBestPath(vCurrTile, aUnitStartTile)
                        return vEndTile
                    elif vTile.mInPathing:
                        if vTile == aEndTile:
                            if not vFindOneBefore:
                                vTile.mPathParent = vCurrTile
                                vTile.mGCost = vCurrTile.mGCost + vUnit.mTerrainDict[vTile.mType]
                                vEndTile = self.makeBestPath(aEndTile, aUnitStartTile)
                                return vEndTile
                        elif vTile.mPathParent is None:
                            vTile.mPathParent = vCurrTile
                            vTile.mGCost = vCurrTile.mGCost + vUnit.mTerrainDict[vTile.mType]
                            vTile.mHCost = abs(aEndTile.x - vTile.x) + abs(aEndTile.y - vTile.y)
                            vFCost = vTile.mGCost + vTile.mHCost
                            heappush(vFrontier, (vFCost, vTile))
                        elif vTile.mPathParent.mGCost > vCurrTile.mGCost:
                            vTile.mGCost = vCurrTile.mGCost + vUnit.mTerrainDict[vTile.mType]
                            vFCost = vTile.mGCost + vTile.mHCost
                            heappush(vFrontier, (vFCost, vTile))


    def makeBestPath(self, aEndTile, aStartTile):
        import sprites
        vCurrTile = aEndTile
        vDirectionFrom = None
        if vCurrTile.mPathParent == vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x + 1, vCurrTile.y), None):
            sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayEndIcon')
            vDirectionFrom = 'left'
        elif vCurrTile.mPathParent == vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x - 1, vCurrTile.y), None):
            sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayEndIcon')
            vDirectionFrom = 'right'
        elif vCurrTile.mPathParent == vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x, vCurrTile.y + 1), None):
            sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayEndIcon')
            vDirectionFrom = 'up'
        elif vCurrTile.mPathParent == vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x, vCurrTile.y - 1), None):
            sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayEndIcon')
            vDirectionFrom = 'down'

        while vDirectionFrom != 'FINISHED':
            vCurrTile = vCurrTile.mPathParent

            if vCurrTile == aStartTile:
                sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'blankTile')
                vDirectionFrom = 'FINISHED'

            elif vCurrTile.mPathParent == vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x + 1, vCurrTile.y), None):
                if vDirectionFrom == 'left' or vDirectionFrom == 'right':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayIcon')
                elif vDirectionFrom == 'up':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayCornerIcon270')
                elif vDirectionFrom == 'down':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayCornerIcon180')
                vDirectionFrom = 'left'

            elif vCurrTile.mPathParent == vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x - 1, vCurrTile.y), None):
                if vDirectionFrom == 'left' or vDirectionFrom == 'right':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayIcon')
                elif vDirectionFrom == 'up':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayCornerIcon')
                elif vDirectionFrom == 'down':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayCornerIcon90')
                vDirectionFrom = 'right'

            elif vCurrTile.mPathParent == vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x, vCurrTile.y + 1), None):
                if vDirectionFrom == 'up' or vDirectionFrom == 'down':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayIcon90')
                elif vDirectionFrom == 'left':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayCornerIcon90')
                elif vDirectionFrom == 'right':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayCornerIcon180')
                vDirectionFrom = 'up'

            elif vCurrTile.mPathParent == vCurrTile.mGame.mMap.mTileDict.get((vCurrTile.x, vCurrTile.y - 1), None):
                if vDirectionFrom == 'up' or vDirectionFrom == 'down':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayIcon90')
                elif vDirectionFrom == 'left':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayCornerIcon')
                elif vDirectionFrom == 'right':
                    sprites.PathDisplayTile(vCurrTile.mGame, vCurrTile, 'pathDisplayCornerIcon270')
                vDirectionFrom = 'down'

        return aEndTile


class FogTile( TerrrainTile ):
    def __init__( self, aGame, aXPos, aYPos ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllTerrainGroup, aGame.mAllCameraCollideGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.mType = TerrainTypes.fogTile
        self.image = spritesImageDict[self.mType]
        self.rect = self.image.get_rect()
        self.x = aXPos
        self.y = aYPos
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mIsSelected = False
        self.mIsAvailable = True
        self.mInPathing = False
        self.mPathParent = None
        self.mHCost = None
        self.mGCost = None
        self.mUnit = None

    def update( self ):
        pass

class WaterTile( TerrrainTile ):
    def __init__( self, aGame, aXPos, aYPos ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllTerrainGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.mType = TerrainTypes.waterTile
        self.image = spritesImageDict[self.mType]
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.x = aXPos
        self.y = aYPos
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mIsSelected = False
        self.mIsAvailable = True
        self.mInPathing = False
        self.mPathParent = None
        self.mHCost = None
        self.mGCost = None
        self.mUnit = None

    def update( self ):
        pass

class GrassTile( TerrrainTile ):
    def __init__( self, aGame, aXPos, aYPos ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllTerrainGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.mType = TerrainTypes.grassTile
        self.image = spritesImageDict[self.mType]
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.x = aXPos
        self.y = aYPos
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mIsSelected = False
        self.mIsAvailable = True
        self.mInPathing = False
        self.mPathParent = None
        self.mHCost = None
        self.mGCost = None
        self.mUnit = None

class PlainTile( TerrrainTile ):
    def __init__( self, aGame, aXPos, aYPos ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllTerrainGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.mType = TerrainTypes.plainTile
        self.image = spritesImageDict[self.mType]
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.x = aXPos
        self.y = aYPos
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mIsSelected = False
        self.mIsAvailable = True
        self.mInPathing = False
        self.mPathParent = None
        self.mHCost = None
        self.mGCost = None
        self.mUnit = None

    def update( self ):
        pass

class MountainTile( TerrrainTile ):
    def __init__( self, aGame, aXPos, aYPos ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllTerrainGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.mType = TerrainTypes.mountainTile
        self.image = spritesImageDict[self.mType].convert_alpha()
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.x = aXPos
        self.y = aYPos
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mIsSelected = False
        self.mIsAvailable = True
        self.mInPathing = False
        self.mPathParent = None
        self.mHCost = None
        self.mGCost = None
        self.mUnit = None

    def update( self ):
        pass

class ForestTile( TerrrainTile ):
    def __init__( self, aGame, aXPos, aYPos ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllTerrainGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.mType = TerrainTypes.forestTile
        self.image = spritesImageDict[self.mType]
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.x = aXPos
        self.y = aYPos
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mIsSelected = False
        self.mIsAvailable = True
        self.mInPathing = False
        self.mPathParent = None
        self.mHCost = None
        self.mGCost = None
        self.mUnit = None

    def update( self ):
        pass

class CityTile( TerrrainTile ):
    def __init__( self, aGame, aXPos, aYPos, aPlayerId = None ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllTerrainGroup
        pg.sprite.Sprite.__init__( self, self.mGroups )
        self.mGame = aGame
        self.mType = TerrainTypes.cityTile
        self.image = spritesImageDict[self.mType].convert_alpha()
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.x = aXPos
        self.y = aYPos
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mIsSelected = False
        self.mIsAvailable = True
        self.mInPathing = False
        self.mPathParent = None
        self.mHCost = None
        self.mGCost = None
        self.mUnit = None
        # owner must be updated when a city gets capped
        self.mOwner = None
        self.mPlayerId = aPlayerId

        if self.mPlayerId != None:
            self.updateOwnerStatus( self.mPlayerId )

    def updateOwnerStatus( self, aNewPlayerId ):
        self.mPlayerId = aNewPlayerId
        if self.mPlayerId != None:
            if self.mOwner != None:
                self.mOwner.mCitiesOwned.remove( self )
            self.mOwner = self.mGame.mPlayers[self.mPlayerId]
            self.mOwner.mCitiesOwned.append( self )

            vCityType = player.playerIdCityTypeDict[self.mPlayerId]
            self.image = spritesImageDict[vCityType]
            self.mOrigImage = self.image

    def update( self ):
        pass