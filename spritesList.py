import pygame as pg
from enum import Enum

class TerrainTypes( Enum ):
    fogTile = 0
    waterTile = 10
    grassTile = 11
    plainTile = 12
    mountainTile = 13
    forestTile = 14
    redCityTile = 20
    blueCityTile = 21
    # greenCityTile = 21 # future colours
    # purpleCityTile = 21 # future colours
    cityTile = 30



# this is where all the objects will be mapped to their image
# this is a python dict, where if you provide a key, it will give you the value
# in this case, we will map string keys to pygame load methods
# ex: 'soldier' : pg.image.load("soldier.png")
# if you refer to this dict with the soldier key, it will load the image soldier.png
spritesImageDict = {
    # terrain tile images
    TerrainTypes.fogTile : pg.image.load( "graphics\\terrain\\fog.png" ),
    TerrainTypes.waterTile : pg.image.load( "graphics\\terrain\\water.png" ),
    TerrainTypes.grassTile : pg.image.load( "graphics\\terrain\\grass.png" ),
    TerrainTypes.plainTile : pg.image.load( "graphics\\terrain\\fields.png" ),
    TerrainTypes.mountainTile : pg.image.load( "graphics\\terrain\\mountain.png" ),
    TerrainTypes.forestTile : pg.image.load( "graphics\\terrain\\forest.png" ),
    TerrainTypes.cityTile : pg.image.load( 'graphics\\buildings\\city1.png' ),
    TerrainTypes.redCityTile : pg.image.load( 'graphics\\buildings\\city1red.png' ),
    TerrainTypes.blueCityTile : pg.image.load( 'graphics\\buildings\\city1blue.png' ),

    # flags
    'RedFlag' : pg.image.load( 'graphics\\buildings\\capturedFlagRed.png' ),
    'BlueFlag' : pg.image.load( 'graphics\\buildings\\capturedFlagBlue.png' ),
    # other flags too when added

    # health markers
    '10hp' : pg.image.load( "graphics\\units\\health\\10healthl.png" ),
    '9hp' : pg.image.load( "graphics\\units\\health\\9healthl.png" ),
    '8hp' : pg.image.load( "graphics\\units\\health\\8healthl.png" ),
    '7hp' : pg.image.load( "graphics\\units\\health\\7healthl.png" ),
    '6hp' : pg.image.load( "graphics\\units\\health\\6healthl.png" ),
    '5hp' : pg.image.load( "graphics\\units\\health\\5healthl.png" ),
    '4hp' : pg.image.load( "graphics\\units\\health\\4healthl.png" ),
    '3hp' : pg.image.load( "graphics\\units\\health\\3healthl.png" ),
    '2hp' : pg.image.load( "graphics\\units\\health\\2healthl.png" ),
    '1hp' : pg.image.load( "graphics\\units\\health\\1healthl.png" ),

    # units
    'infantry' : pg.image.load( "graphics\\units\\infantry.png" ),
    'BattleshipBlue' : pg.image.load( "graphics\\units\\battleshipBlue.png" ),
    'BattleshipRed' : pg.image.load( "graphics\\units\\battleshipRed.png" ),
    'LightInfantryBlue' : pg.image.load( "graphics\\units\\lightInfantryBlue.png" ),
    'LightInfantryRed' : pg.image.load( "graphics\\units\\lightInfantryRed.png" ),

    # red walking
    'LightInfantryRedWalking0' : pg.image.load( "graphics\\units\\lightInfantryRedWalking0.png" ),
    'LightInfantryRedWalking1' : pg.image.load( "graphics\\units\\lightInfantryRedWalking1.png" ),
    'LightInfantryRedWalking2' : pg.image.load( "graphics\\units\\lightInfantryRedWalking2.png" ),
    'LightInfantryRedWalking3' : pg.image.load( "graphics\\units\\lightInfantryRedWalking3.png" ),

    # blue walking
    'LightInfantryBlueWalking0' : pg.image.load( "graphics\\units\\lightInfantryRedWalking0.png" ), # todo change to blue
    'LightInfantryBlueWalking1' : pg.image.load( "graphics\\units\\lightInfantryRedWalking1.png" ),
    'LightInfantryBlueWalking2' : pg.image.load( "graphics\\units\\lightInfantryRedWalking2.png" ),
    'LightInfantryBlueWalking3' : pg.image.load( "graphics\\units\\lightInfantryRedWalking3.png" ),

    # red attacking
    'LightInfantryRedAttacking0' : pg.image.load( "graphics\\units\\lightInfantryRed.png" ),
    'LightInfantryRedAttacking1' : pg.image.load( "graphics\\units\\lightInfantryRedAttacking0.png" ),
    'LightInfantryRedAttacking2' : pg.image.load( "graphics\\units\\lightInfantryRedAttacking1.png" ),
    'LightInfantryRedAttacking3' : pg.image.load( "graphics\\units\\lightInfantryRedAttacking2.png" ),
    'LightInfantryRedAttacking4' : pg.image.load( "graphics\\units\\lightInfantryRedAttacking3.png" ),

    # blue attacking
    'LightInfantryBlueAttacking0' : pg.image.load( "graphics\\units\\lightInfantryRed.png" ),
    'LightInfantryBlueAttacking1' : pg.image.load( "graphics\\units\\lightInfantryRedAttacking0.png" ), # todo change to blue
    'LightInfantryBlueAttacking2' : pg.image.load( "graphics\\units\\lightInfantryRedAttacking1.png" ),
    'LightInfantryBlueAttacking3' : pg.image.load( "graphics\\units\\lightInfantryRedAttacking2.png" ),
    'LightInfantryBlueAttacking4' : pg.image.load( "graphics\\units\\lightInfantryRedAttacking3.png" ),

    # red defending
    'LightInfantryRedDefending0' : pg.image.load( "graphics\\units\\lightInfantryRed.png" ),
    'LightInfantryRedDefending1' : pg.image.load( "graphics\\units\\lightInfantryRedDefending0.png" ),
    'LightInfantryRedDefending2' : pg.image.load( "graphics\\units\\lightInfantryRedDefending0.png" ),
    'LightInfantryRedDefending3' : pg.image.load( "graphics\\units\\lightInfantryRedDefending0.png" ),
    'LightInfantryRedDefending4' : pg.image.load( "graphics\\units\\lightInfantryRedDefending0.png" ),

    # red defending
    'LightInfantryBlueDefending0' : pg.image.load( "graphics\\units\\lightInfantryRed.png" ),
    'LightInfantryBlueDefending1' : pg.image.load( "graphics\\units\\lightInfantryRedDefending0.png" ),
    'LightInfantryBlueDefending2' : pg.image.load( "graphics\\units\\lightInfantryRedDefending0.png" ),
    'LightInfantryBlueDefending3' : pg.image.load( "graphics\\units\\lightInfantryRedDefending0.png" ),
    'LightInfantryBlueDefending4' : pg.image.load( "graphics\\units\\lightInfantryRedDefending0.png" ),
    
    # red fUcKInG DiEIng
    'LightInfantryRedDeath0' : pg.image.load( "graphics\\units\\lightInfantryRed.png" ),
    'LightInfantryRedDeath1' : pg.image.load( "graphics\\units\\lightInfantryRedDeath0.png" ),
    'LightInfantryRedDeath2' : pg.image.load( "graphics\\units\\lightInfantryRedDeath1.png" ),
    'LightInfantryRedDeath3' : pg.image.load( "graphics\\units\\lightInfantryRedDeath2.png" ),
    'LightInfantryRedDeath4' : pg.image.load( "graphics\\units\\lightInfantryRedDeath3.png" ),
    'LightInfantryRedDeath5' : pg.image.load( "graphics\\units\\lightInfantryRedDeath4.png" ),
    
    # blue fUcKInG DiEIng
    'LightInfantryBlueDeath0' : pg.image.load( "graphics\\units\\lightInfantryRed.png" ),
    'LightInfantryBlueDeath1' : pg.image.load( "graphics\\units\\lightInfantryRedDeath0.png" ),
    'LightInfantryBlueDeath2' : pg.image.load( "graphics\\units\\lightInfantryRedDeath1.png" ),
    'LightInfantryBlueDeath3' : pg.image.load( "graphics\\units\\lightInfantryRedDeath2.png" ),
    'LightInfantryBlueDeath4' : pg.image.load( "graphics\\units\\lightInfantryRedDeath3.png" ),
    'LightInfantryBlueDeath5' : pg.image.load( "graphics\\units\\lightInfantryRedDeath4.png" ),

    # overlay images
	'blankTile' : pg.image.load( "graphics\\terrain\\blank.png"),
	'selectorIcon' : pg.image.load( "graphics\\terrain\\selecting.png" ),
    'selectedIcon' : pg.image.load( "graphics\\terrain\\selected.png"),
    'pathingIcon' : pg.image.load( "graphics\\terrain\\pathing.png" ),
    'attackIcon' : pg.image.load( "graphics\\terrain\\attackable.png" ),
    'targettedIcon' : pg.image.load( "graphics\\terrain\\targetted.png" ),
    'pathDisplayIcon': pg.image.load( "graphics\\terrain\\selectingPath.png" ),
    'pathDisplayIcon90': pg.image.load( "graphics\\terrain\\selectingPath90.png" ),
    'pathDisplayCornerIcon': pg.image.load( "graphics\\terrain\\selectingPathCorner.png" ),
    'pathDisplayCornerIcon90': pg.image.load( "graphics\\terrain\\selectingPathCorner90.png" ),
    'pathDisplayCornerIcon180': pg.image.load( "graphics\\terrain\\selectingPathCorner180.png" ),
    'pathDisplayCornerIcon270': pg.image.load( "graphics\\terrain\\selectingPathCorner270.png" ),
    'pathDisplayEndIcon': pg.image.load( "graphics\\terrain\\selectingPathEnd.png" ),

    'camera' : pg.image.load( "graphics\\units\\cam.png" ),
}