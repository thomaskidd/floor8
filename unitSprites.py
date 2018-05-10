import pygame as pg
from settings import *
from spritesList import *
from keybindings import *
from movementDicts import *
import player
import math
import attackDict

class Unit( pg.sprite.Sprite ):
    def __init__( self ):
        pass

    def eventHandle( self, aAction ):
        pass

    def saveHelper( self ):
        vInfo = ( self.mName, ( self.x, self.y ), self.mPlayerId, self.mHealth, self.mLevel )
        return vInfo

    def moveToTile( self, aTile ):
        vRv = False
        if ( aTile.mInPathing == False ) or not ( self.mGame.mCurrentPlayerTurn == self.mPlayerId ):
            if self.mGame.mVerbosity >= 2:
                print('self.mGame.mCurrentPlayerTurn', self.mGame.mCurrentPlayerTurn)
                print('self.mPlayerId', self.mPlayerId)
            vRv = False
        else:
            self.mMovesLeft -= self.mChangeInMoves
            # queue movement animation
            self.mAnimationQueue.queue('MOVE')
            self.mTile = aTile
            # let the tile know the unit is on it
            self.mTile.mIsAvailable = False
            self.mTile.mUnit = self
            self.mGame.cleanUpPathingTiles()
            self.mGame.cleanUpTargetTiles()
            # capture it if it's a city tile
            if self.mTile.mType == TerrainTypes.cityTile:
                self.captureCity()
            vRv = True
        return vRv

    def updatePos( self ):
        self.x = self.mTile.x
        self.y = self.mTile.y
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE
        self.mHealthBar.updateHealthBarPos()

    def captureCity( self ):
        # self.mTile.mPlayerId = self.mPlayerId
        self.mTile.updateOwnerStatus( self.mPlayerId )

    def calculateVeterancyBonus( self, aLevel ):
        vStrengthMultiplier = math.sqrt( float(aLevel)/80. ) + 1
        if self.mGame.mVerbosity >= 5:
            print('vStrengthMultiplier', vStrengthMultiplier)
        return float( vStrengthMultiplier )

    def setUpStatsWithBonuses( self ):
        # stats
        # health
        vName = self.mName
        vHealthMultiplier = self.mOwner.mUnitBonuses[vName + 'HealthBonusPercent']
        vHealthFlatBonus = self.mOwner.mUnitBonuses[vName + 'HealthBonusFlat']
        self.mHealth = ( self.mHealth * vHealthMultiplier ) + vHealthFlatBonus
        self.mMaxHealth = self.mHealth

        #movement range
        self.mRange = self.mRange + self.mOwner.mUnitBonuses[vName + 'BonusMove']
        if self.mGame.mVerbosity >= 3 :
            print('self.mRange', self.mRange)

        # unit strength
        vLevelBonus = self.calculateVeterancyBonus( self.mLevel )
        self.mAttackDamage = ( self.mAttackDamage * self.mOwner.mUnitBonuses[vName + 'AttackDamagePercent']\
                                 * vLevelBonus ) + self.mOwner.mUnitBonuses[vName + 'AttackDamageFlat']
        if self.mGame.mVerbosity >= 3 :
            print( 'self.mAttackDamage', self.mAttackDamage )

        self.mArmourPiercingDamage = ( self.mArmourPiercingDamage * self.mOwner.mUnitBonuses[vName + 'APBonusPercent'] )\
                                     + self.mOwner.mUnitBonuses[vName + 'APBonusFlat']

        self.mArmour = (self.mArmour * self.mOwner.mUnitBonuses[vName + 'ArmourBonusPercent']) \
                                     + self.mOwner.mUnitBonuses[vName + 'ArmourBonusFlat']

    def findAttackRange( self ):
        self.mGame.cleanUpTargetTiles()
        if self.mNumberOfAttacks > 0:
            for vTile in self.mGame.mAllTerrainGroup:
                if vTile != self.mTile and vTile.mType != TerrainTypes.fogTile:
                    vX = self.mTile.x - vTile.x
                    vY = self.mTile.y - vTile.y
                    vH = math.sqrt( (vX**2 + vY**2) ) # good ol pythagoras
                    if vH <= self.mAttackRangeMax and vH >= self.mAttackRangeMin:
                        import sprites
                        if self.allCheck( vTile.mUnit, vTile ):
                            sprites.AttackTile(self.mGame, vTile)
                            sprites.TargettedTile(self.mGame, vTile)
                            vTile.mUnit.mIsTargetted = True
                        elif self.mAttackRangeMax > 1:
                            sprites.AttackTile(self.mGame, vTile)

    def attack( self, aTargettedUnit ):
        self.mGame.cleanUpPathingTiles()
        self.mGame.cleanUpTargetTiles()
        # reduce number of attacks and set moves left to zero
        self.mNumberOfAttacks -= 1
        # change this if you want it to be able to move after attack?
        self.mMovesLeft = 0
        # animation queueing
        vAttackDirection = self.findAttackDirection( aTargettedUnit )
        self.mAnimationQueue.queue(vAttackDirection)
        aTargettedUnit.mAnimationQueue.queue(Animation.DEFENDING)
        # deal damage
        vAttackValue = self.findDamage( aTargettedUnit )
        aTargettedUnit.mDamageTaken -= vAttackValue

        if aTargettedUnit.mHealth - vAttackValue > 0:
            if self.mAttackType == AttackType.MELEE and aTargettedUnit.mAttackType == AttackType.MELEE:
                # queue next animations
                vAttackDirection = aTargettedUnit.findAttackDirection( aTargettedUnit )
                aTargettedUnit.mAnimationQueue.queue(vAttackDirection)
                self.mAnimationQueue.queue(Animation.DEFENDING)
                # deal damage
                vDamageTaken = aTargettedUnit.findDamage( self )
                self.mDamageTaken -= vDamageTaken

    def findDamage( self, aTargettedUnit ):
        vPercentDamageLostFromMissingHealth = self.mHealth / 50
        vPercentFromElevation = self.mAttackDict[aTargettedUnit.mElevation]
        vAttackValue = ( self.mAttackDamage * vPercentDamageLostFromMissingHealth *
                         vPercentFromElevation ) - aTargettedUnit.mArmour

        if vAttackValue <= 0:
            vAttackValue = 0
        vAttackValue += self.mArmourPiercingDamage
        if self.mGame.mVerbosity >= 2:
            print( 'damage to deal: ', vAttackValue )

        return vAttackValue

    def allCheck( self, aTargetUnits, aTile ):
        vRv = False
        if self.unitExists( aTile ):
            if self.enemyUnitCheck( aTile ):
                if self.validAttackCheck( aTargetUnits ):
                    vRv = True
        return vRv

    def validAttackCheck( self, aTargetedUnit ):
        vCheck = self.mAttackDict[aTargetedUnit.mElevation]
        if vCheck:
            vRv = True
        else:
            vRv = False
        return vRv

    def unitExists( self, aTile ):
        if ( aTile.mUnit != None ):
            vRv = True
        else:
            vRv = False
        return vRv

    def enemyUnitCheck( self, aTile ):
        if aTile.mUnit.mPlayerId != self.mPlayerId:
            vRv = True
        else:
            vRv = False
        return vRv

    def killUnit( self ):
        self.mOwner.mUnits.remove( self )
        self.mTile.mUnit = None
        self.mTile.mIsAvailable = True
        self.mHealthBar.kill()
        self.kill()

    def destinationAnimation( self ):
        # self.mGame.mUnitMoving = self
        self.mPath = self.mGame.mShortestPathList
        self.mDestTile = self.mPath[0]
        # reverse the list, so it's in the right order, from unit to destination
        self.mPath.reverse()
        self.mPath.pop(0)
        self.mFrameCounter = 0
        self.mAnimationIdx = 0
        self.mPathTileIdx = 0
        self.findDirection(aIsInitial = True)

    def createAnimationStringList( self, aPrependStr, aLen ):
        vRv = []
        for vX in range( aLen ):
            vImageStr = ''.join( ( self.mImageStr, aPrependStr, str( vX ) ) )
            vRv.append( vImageStr )
        return vRv

    def findDirection( self, aIsInitial = False ):
        if self.mPathTileIdx < len(self.mPath) - 1:
            if not aIsInitial:
                self.mPathTileIdx += 1
            vCurTile = self.mPath[self.mPathTileIdx]
            if self.mPathTileIdx >= len(self.mPath) - 1:
                vNextTile = self.mPath[len(self.mPath) - 1]
            else:
                vNextTile = self.mPath[self.mPathTileIdx + 1]

            if vCurTile.x < vNextTile.x:
                self.mAnimationState = Animation.MOVINGRIGHT
            elif vCurTile.x > vNextTile.x:
                self.mAnimationState = Animation.MOVINGLEFT
            elif vCurTile.y < vNextTile.y:
                self.mAnimationState = Animation.MOVINGDOWN
            elif vCurTile.y > vNextTile.y:
                self.mAnimationState = Animation.MOVINGUP
        # this means it's reached it's destination
        else:
            self.mAnimationState = self.mAnimationQueue.updateAction()
            self.updatePos()

    # updates units position and checks for overshooting tiles
    def animateMovement( self, aNextTile, aXDirection, aYDirection ):
        if aXDirection != 0:
            # this checks if the unit passes its next tile
            # I know it's gross but just trust me it works
            if (aXDirection * ( self.x + ( aXDirection * Settings.MOVESPEED ) )) < ( aXDirection * aNextTile.x ):
                self.x += ( aXDirection * Settings.MOVESPEED )
                self.rect.x = self.x * self.mGame.mCurrentTileSize 
                self.animateHelper(animationRate.MoveAnimationRate, self.mAnimateMoveList)
            else:
                self.overShootUpdate(aNextTile)

        elif aYDirection != 0:
            # this checks if the unit passes its next tile
            # plz forgive me, deni boi made me do it
            if (aYDirection * ( self.y + ( aYDirection * Settings.MOVESPEED ) )) < ( aYDirection * aNextTile.y ):
                self.y += ( aYDirection * Settings.MOVESPEED )
                self.rect.y = self.y * self.mGame.mCurrentTileSize 
                self.animateHelper(animationRate.MoveAnimationRate, self.mAnimateMoveList)
            else:
                self.overShootUpdate(aNextTile)

    # resets tile to next tile, which really becomes the current tile
    def overShootUpdate( self, aNextTile ):
        self.x = aNextTile.x
        self.y = aNextTile.y
        self.rect.x = self.x * self.mGame.mCurrentTileSize
        self.rect.y = self.y * self.mGame.mCurrentTileSize
        self.findDirection()

    def findAttackDirection( self, aTargettedUnit ):
        self.mFrameCounter = 0
        self.mAnimationIdx = 0
        # needs to default to something
        vRv= Animation.ATTACKINGLEFT
        if self.x > aTargettedUnit.x:
            vRv= Animation.ATTACKINGLEFT
        elif self.x < aTargettedUnit.x:
            vRv = Animation.ATTACKINGRIGHT
        if self.y > aTargettedUnit.y :
            vRv = Animation.ATTACKINGUP
        elif self.y < aTargettedUnit.y :
            vRv = Animation.ATTACKINGDOWN
        return vRv

    # handles animation
    def animate( self ):
        if self.mAnimationState == Animation.IDLE:
            self.mAnimationState = self.mAnimationQueue.updateAction()

        if self.mAnimationState == Animation.IDLE:
            self.animateHelper(animationRate.IdleAnimationRate, self.mAnimateMoveList)

        elif self.mAnimationState == Animation.ATTACKINGUP:
            self.animateHelper( animationRate.AttackAnimationRate, self.mAnimateAttackList )

        elif self.mAnimationState == Animation.ATTACKINGRIGHT:
            self.animateHelper( animationRate.AttackAnimationRate, self.mAnimateAttackList )

        elif self.mAnimationState == Animation.ATTACKINGLEFT:
            self.animateHelper( animationRate.AttackAnimationRate, self.mAnimateAttackList )

        elif self.mAnimationState == Animation.ATTACKINGDOWN:
            self.animateHelper( animationRate.AttackAnimationRate, self.mAnimateAttackList )

        elif self.mAnimationState == Animation.DEFENDING:
            # update health bar after defend animation
            self.mHealthBar.updateHealthBar()
            self.animateHelper( animationRate.AttackAnimationRate, self.mAnimateDefendList )

        elif self.mAnimationState == Animation.DEATH:
            self.animateHelper( animationRate.AttackAnimationRate, self.mAnimateDeathList )

        else:
            if self.mPathTileIdx >= len(self.mPath) - 1:
                vNextTile = self.mPath[len(self.mPath) - 1]
            else:
                vNextTile = self.mPath[self.mPathTileIdx + 1]

            if self.mAnimationState == Animation.MOVINGUP:
                self.animateMovement(vNextTile, 0, -1)
            elif self.mAnimationState == Animation.MOVINGDOWN:
                self.animateMovement(vNextTile, 0, 1)
            elif self.mAnimationState == Animation.MOVINGLEFT:
                self.animateMovement(vNextTile, -1, 0)
            elif self.mAnimationState == Animation.MOVINGRIGHT:
                self.animateMovement(vNextTile, 1, 0)

            self.mHealthBar.updateHealthBarPos()

    # runs through animation
    def animateHelper( self, aAnimationRate, aAnimationList ):
        self.mFrameCounter += 1
        vFinishedAnimation = False
        # this updates every frame, but we dont want every animation to change every frame
        # check if it's exceeded its counter
        if self.mFrameCounter >= aAnimationRate:
            if self.mAnimationIdx >= len(aAnimationList):
                self.mAnimationIdx = 0
                # if it's an attack animation, we only want it to run once
                vAttackDefendAnimation = self.mAnimationState in [ Animation.ATTACKINGDOWN,
                                             Animation.ATTACKINGUP,
                                             Animation.ATTACKINGLEFT,
                                             Animation.ATTACKINGRIGHT,
                                             Animation.DEFENDING,
                                             Animation.DEATH]
                if vAttackDefendAnimation:
                    if self.mIsDead == True:
                        self.killUnit()
                    self.mAnimationState = self.mAnimationQueue.updateAction()
            vImageStr = aAnimationList[self.mAnimationIdx]
            self.mOrigImage = spritesImageDict[vImageStr]
            self.mAnimationIdx += 1
            self.mFrameCounter = 0

    def update( self ):
        self.animate()

# cause why not
class AnimationQueue( ):
    def __init__( self, aUnit ):
        self.mUnit = aUnit
        # this should never leave position 0, it is the base of the list
        self.mQueue = [ Animation.IDLE ]

    def queue( self, aAction ):
        if aAction in Animation:
            self.mQueue.append(aAction)
        elif aAction == 'MOVE' or aAction[:7] == 'TRIGGER' or aAction[:7] == 'BLOCKER':
            self.mQueue.append(aAction)
        else:
            print('ERROR: Queueing failed as %s is not a known action.' % aAction)

    # this gets the next action and updates the list
    # always returns an animation state
    def updateAction( self ):
        vRv = self.mQueue[0]
        # the next queued is always in this position because of the IDLE base pos
        curAction = 1
        # if the queue isn't complete (ie only idle remains)
        if len(self.mQueue) > 1:
            self.mUnit.mFrameCounter = 0
            self.mUnit.mAnimationIdx = 0
            vRv = self.mQueue[curAction] 
            if vRv not in Animation:
                if vRv == 'MOVE':
                    self.mQueue.pop(curAction)
                    self.mUnit.destinationAnimation()
                    vRv = self.mUnit.mAnimationState
                elif vRv[:7] == 'TRIGGER':
                    self.mQueue.pop(curAction)
                    self.mUnit.mBlockerGroup.trigger(vRv)
                    vRv = self.updateAction()
                elif vRv[:7] == 'BLOCKER':
                    vRv = self.mUnit.mAnimationState
            else:
                self.mQueue.pop(curAction)

        return vRv

    def clear( self ):
        # clears queued part of list
        self.mQueue[1:] = []

    # remove first action of type aAction in list
    def removeAction( self, aAction ):
        vIdx = 1
        vDone = False
        while not vDone and vIdx < len(self.mQueue):
            vAction = self.mQueue[vIdx]
            if vAction == aAction:
                self.mQueue.pop(vIdx)
                vDone = True

# to be able to put blocks (waits) in animation queues
class BlockerGroup( ):
    def __init__( self, aOwnerUnit ):
        self.mOwnerUnit = aOwnerUnit
        self.mID = str( id(self.mOwnerUnit) )
        self.mTriggerCode = 'TRIGGER' + self.mID
        self.mBlockerCode = 'BLOCKER' + self.mID
        self.mGroup = []

    def createTrigger( self ):
        # return trigger code for animation queue
        self.mOwnerUnit.mAnimationQueue.queue(self.mTriggerCode)

    def createBlocker( self, aBlockedUnit ):
        # add unit to blocked list
        self.mGroup.append(aBlockedUnit)
        # add blocker code for animation queue
        aBlockedUnit.mAnimationQueue.queue(self.mBlockerCode)

    def trigger( self, aTriggerCode ):
        # check that trigger code matches
        if aTriggerCode == self.mTriggerCode:
            # remove all blockers from each blocked units animation queue
            for vBlockedUnit in self.mGroup:
                vBlockedUnit.mAnimationQueue.removeAction(self.mBlockerCode)
            self.clear()
        else:
            print('ERROR: Trigger found in a mismatched unit.')

    def clear( self ):
        self.mGroup[:] = []

class LightInfantry( Unit ):
    def __init__( self, aGame, aTile, aPlayerId, aHealth, aLevel ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllUnitsGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.mPlayerId = aPlayerId

        vColourStr = player.playerIdColourDict[self.mPlayerId]
        self.mOwner = aGame.mPlayers[self.mPlayerId]
        self.mOwner.mUnits.append( self )
        self.mName = 'LightInfantry'
        self.mElevation = WhereThouDothReside.GROUND

        # images and rects
        self.mImageStr = self.mName + vColourStr
        self.image = spritesImageDict[self.mImageStr].convert_alpha()
        self.mOrigImage = self.image

        # animation queue and state
        self.mAnimationQueue = AnimationQueue(self)
        self.mBlockerGroup = BlockerGroup(self)
        self.mAnimationState = self.mAnimationQueue.updateAction()

        self.mFrameCounter = 0
        self.mAnimationIdx = 0
        self.mAnimateMoveList = []
        self.mAnimateAttackList = []
        self.mAnimateDefendList = []
        self.mAnimateMoveList = self.createAnimationStringList( 'Walking', 4 )
        self.mAnimateAttackList = self.createAnimationStringList( 'Attacking', 5 )
        self.mAnimateDefendList = self.createAnimationStringList( 'Defending', 5 )
        self.mAnimateDeathList = self.createAnimationStringList('Death', 6)

        self.rect = self.image.get_rect()
        self.mTile = aTile
        self.x = self.mTile.x
        self.y = self.mTile.y
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE

        self.mTerrainDict = movementDicts[self.mName]
        self.mAttackDict = attackDict.gAttackDict[self.mName]

        # set up default stats here
        self.mLevel = aLevel
        self.mAttackType = AttackType.MELEE
        self.mRange = 10
        self.mChangeInMoves = 0
        self.mMovesLeft = self.mRange
        self.mNumberOfAttacks = 1
        self.mAttackRangeMax = 1
        self.mAttackRangeMin = 0
        self.mHealth = aHealth
        self.mMaxHealth = aHealth
        self.mDamageTaken = 0
        self.mAttackDamage = 10
        self.mArmourPiercingDamage = 1
        self.mArmour = 2
        self.setUpStatsWithBonuses()

        # set up health bars
        self.mHealthBar = HealthBars( self.mGame, self )
        self.mHealthBar.updateHealthBar()

        # states
        self.mIsSelected = False
        self.mIsTargetted = False
        self.mIsTargettedOutOfRange = False
        self.mIsDead = False

        # let tile know what unit is on it
        self.mTile.mIsAvailable = False
        self.mTile.mUnit = self

class Battleship( Unit ):
    def __init__( self, aGame, aTile, aPlayerId, aHealth, aLevel ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllUnitsGroup
        pg.sprite.Sprite.__init__(self, self.mGroups)
        self.mGame = aGame
        self.mPlayerId = aPlayerId

        vColourStr = player.playerIdColourDict[self.mPlayerId]
        self.mOwner = aGame.mPlayers[self.mPlayerId]
        self.mOwner.mUnits.append(self)
        self.mName = 'Battleship'

        self.mElevation = WhereThouDothReside.WATER

        # images and rects
        self.mImageStr = self.mName + vColourStr
        self.image = spritesImageDict[self.mImageStr].convert_alpha()
        self.mOrigImage = self.image

        # animation queue and state
        self.mAnimationQueue = AnimationQueue(self)
        self.mBlockerGroup = BlockerGroup(self)
        self.mAnimationState = self.mAnimationQueue.updateAction()

        self.mFrameCounter = 0
        self.mAnimationIdx = 0
        #todo fix this garbage
        self.mAnimateMoveList = [self.mImageStr]
        self.mAnimateAttackList = [self.mImageStr]
        self.mAnimateDefendList = [self.mImageStr]

        self.rect = self.image.get_rect()
        self.mTile = aTile
        self.x = self.mTile.x
        self.y = self.mTile.y
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE

        self.mTerrainDict = movementDicts[self.mName]
        self.mAttackDict = attackDict.gAttackDict[self.mName]

        # stats
        self.mLevel = aLevel
        self.mAttackType = AttackType.INDIRECT
        self.mRange = 3
        self.mMovesLeft = self.mRange
        self.mChangeInMoves = 0
        self.mNumberOfAttacks = 1
        self.mAttackRangeMax = 4.5
        self.mAttackRangeMin = 0
        self.mHealth = aHealth
        self.mMaxHealth = aHealth
        self.mDamageTaken = 0
        self.mAttackDamage = 20
        self.mArmourPiercingDamage = 1
        self.mArmour = 5
        self.setUpStatsWithBonuses()

        # set up health bar
        self.mHealthBar = HealthBars( self.mGame, self )
        self.mHealthBar.updateHealthBar()

        # states
        self.mIsSelected = False
        self.mIsTargetted = False
        self.mIsTargettedOutOfRange = False
        self.mIsDead = False

        # let tile know what unit is on it
        self.mTile.mIsAvailable = False
        self.mTile.mUnit = self

class HealthBars( pg.sprite.Sprite ):
    def __init__( self, aGame, aUnit ):
        self.mGroups = aGame.mAllSpritesGroup, aGame.mAllHealthBarsGroup
        pg.sprite.Sprite.__init__( self, self.mGroups )
        self.mGame = aGame
        self.mUnit = aUnit

        self.mHealth = self.mUnit.mHealth
        # images and rects
        self.image = None
        self.findNewImage()
        self.mOrigImage = self.image
        self.rect = self.image.get_rect()
        self.x = self.mUnit.x
        self.y = self.mUnit.y
        self.rect.x = self.x * Settings.TILESIZE
        self.rect.y = self.y * Settings.TILESIZE

    def updateHealthBar( self ):
        vChangeInHealth = self.mUnit.mDamageTaken
        self.mUnit.mDamageTaken = 0
        if vChangeInHealth:
            self.mUnit.mHealth += vChangeInHealth
            self.mHealth = self.mUnit.mHealth
            if self.mHealth <= 0:
                self.mUnit.mIsDead = True
                # override animation queue and just kill the fucker
                self.mUnit.mAnimationQueue.clear()
                self.mUnit.mAnimationState = Animation.DEATH
                
            else:
                self.findNewImage()
        self.updateHealthBarPos()

    def updateHealthBarPos( self ):
        self.x = self.mUnit.x
        self.y = self.mUnit.y

    def findNewImage( self ):
        vHealthFraction = float( self.mHealth ) / 10.
        vHealthFraction = math.ceil( vHealthFraction )
        vImgNameStr = '%dhp' % vHealthFraction

        self.image = spritesImageDict[vImgNameStr]
        self.mOrigImage = self.image