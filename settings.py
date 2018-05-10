from enum import Enum, IntEnum

#fullscreen settings
class FullscreenSettings( Enum ):
    WINDOWED = 0
    FULLSCREEN = 1
    BORDERLESS_WINDOW = 2

#gamestate
class GameState( Enum ):
    LOADING = 0
    MAINMENU = 1
    EDITOR = 2
    HUMANPLAYER = 10
    # PLAYER1 = 11
    # PLAYER2 = 12
    # PLAYER3 = 13
    # PLAYER4 = 14
    COMPUTER = 15
    ANIMATION = 20

class Animation( IntEnum ):
    MOVINGUP = 0
    MOVINGDOWN = 1
    MOVINGLEFT = 2
    MOVINGRIGHT = 3
    ATTACKINGUP = 10
    ATTACKINGDOWN = 11
    ATTACKINGRIGHT = 12
    ATTACKINGLEFT = 13
    DEFENDING = 5
    DEATH = 6
    IDLE = 7
    NOTANIMATING = 8


class WhereThouDothReside( Enum ):
    HIGHAIR = 0
    LOWAIR = 1
    GROUND = 2
    WATER = 3
    SUBMERGED = 4

INGAMESTATES = [GameState.HUMANPLAYER,
                    # GameState.PLAYER1,
                    # GameState.PLAYER2,
                    # GameState.PLAYER3,
                    # GameState.PLAYER4,
                    GameState.COMPUTER,
                    ]
class AttackType( Enum ):
    MELEE = 0
    INDIRECT = 1

class Settings():
    # define some colors (R, G, B)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARKGREY = (40, 40, 40)
    LIGHTGREY = (100, 100, 100)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    # Window title
    TITLE = "FLOORATE" #TODO Get a better name

    KEY_INPUT_DELAY = 1
    KEY_INPUT_INPUT_INTERVAL = 100

    TILESIZE = 32
    DEFAULT_DISPLAY_SETTING = FullscreenSettings.WINDOWED
    DISPLAY_SETTING = DEFAULT_DISPLAY_SETTING

    WIDTH = 1024
    HEIGHT = 768
    FPS = 30
    BGCOLOR = DARKGREY

    GRIDWIDTH = WIDTH / TILESIZE
    GRIDHEIGHT = HEIGHT / TILESIZE

    BORDERWIDTH = 200

    MOVESPEED = 0.1

    CAMERASPEED = 9
    ZOOMCAMERASPEEDEXPONENT = 3

    @staticmethod
    def setWidth( aWidth ):
        Settings.WIDTH = aWidth

    @staticmethod
    def setHeight( aHeight ):
        Settings.HEIGHT = aHeight

    @staticmethod
    def setFPS( aFPS ):
        Settings.FPS = aFPS

class animationRate( IntEnum ):
    IdleAnimationRate = Settings.FPS
    MoveAnimationRate = Settings.FPS / 6
    AttackAnimationRate = Settings.FPS / 8

class saveGames( IntEnum ):
    AutoSave = 0
    SaveGame1 = 1
    SaveGame2 = 2

gSaveGameDict = {
    saveGames.AutoSave : 'maps\\autosave.map',
    saveGames.SaveGame1 : 'maps\\savegame1.map',
    saveGames.SaveGame2 : 'maps\\savegame2.map',
}