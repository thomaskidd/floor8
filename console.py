# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

import pygame as pg
import sprites

def takeInput( self ):
    while(1) :
        vIn = input( 'Input a command, ? for help: ' )
        parseInput( self, vIn )
        if vIn in ['', 'exit']:
            return False
        if self.inConsoleSkipFrame is True:
            return True
def parseInput( self, aInput ):
    vIn = aInput
    if vIn is '?':
        print( """
        COMMAND LIST:
create <Unit Class Name>
To spawn a unit, type in create + the unit name. You will be prompted with arg input after.
If you just leave it blank and hit enter right away, defaults will be used 
Ex: create LightInfantry

heal <int to heal>
The unit selected will be healed by x amount
Ex: heal 10

sethp <int to set hp to>
The unit selected will hae its hp set to x 
Ex: sethp 10
""" )
    elif vIn.startswith('create'):
        vNameIdx = vIn.find(' ') + 1
        vConstructor = vIn[vNameIdx:]
        try:
            vXPos = int( input( 'Input X: ' ) )
            vYPos = int( input( 'Input Y: ' ) )
            vPlayerId = int( input( 'Player: ' ) )
            vHealth = int( input( 'Health: ' ) )
            vLevel = int( input( 'Level: ' ) )
            vValidArgs = True
        except:
            vValidArgs = False
            print('invalid args sorry m8')
        if vValidArgs:
            try:
                vUnitConstructor = getattr( sprites, vConstructor )
                vTile = self.mMap.mTileDict[(vXPos, vYPos)]
                vUnitConstructor( self, vTile, vPlayerId, vHealth, vLevel )
                print( 'Creating level %d %s at location (%d,%d), owned by player %d, with %d health' % (
                vLevel, vConstructor, vXPos, vYPos, vPlayerId, vHealth) )
                self.inConsoleSkipFrame = True
            except:
                print("Something went wrong  ¯\_('o')_/¯ ")
    elif vIn.startswith('heal'):
        vNameIdx = vIn.find( ' ' ) + 1
        vToHeal = vIn[vNameIdx:]
        try:
            vXPos = int( input( 'Input X: ' ) )
            vYPos = int( input( 'Input Y: ' ) )
            vValidArgs = True
        except:
            vValidArgs = False
            print('invalid args sorry m8')
        if vValidArgs :
            try :
                vTile = self.mMap.mTileDict[(vXPos, vYPos)]
                vUnit = vTile.mUnit
                vUnit.mHealthBar.updateHealthBar( int(vToHeal) )
                self.inConsoleSkipFrame = True
            except :
                print( "Something went wrong  ¯\_('o')_/¯ " )
    elif vIn.startswith('sethp'):
        vNameIdx = vIn.find( ' ' ) + 1
        vToHeal = vIn[vNameIdx:]
        try:
            vXPos = int( input( 'Input X: ' ) )
            vYPos = int( input( 'Input Y: ' ) )
            vValidArgs = True
        except:
            vValidArgs = False
            print('invalid args sorry m8')
        if vValidArgs :
            try :
                vTile = self.mMap.mTileDict[(vXPos, vYPos)]
                vUnit = vTile.mUnit
                vDifference = int(vToHeal) - vUnit.mHealth
                vUnit.mHealthBar.updateHealthBar( int(vDifference) )
                self.inConsoleSkipFrame = True
            except :
                print( "Something went wrong  ¯\_('o')_/¯ " )
    elif vIn == 'pass' :
        self.inConsoleSkipFrame = True