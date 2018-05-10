# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

import pygame as pg
from settings import *
from keybindings import *
import console

def eventHandling( aGame ):

    vKeyPressed = pg.key.get_pressed()
    vAltHeld = vKeyPressed[pg.K_LALT]

    vFoundTile = False
    vAction = EventActions.NoEvent

    for vEvent in pg.event.get():
        if vEvent.type == pg.QUIT:
            aGame.mInGame = False

        if vEvent.type == pg.VIDEORESIZE:
            vWidth = vEvent.dict['size'][0]
            vHeight = vEvent.dict['size'][1]

            # resize UI variables
            aGame.mGUI.resizeComponents(Settings.WIDTH, Settings.HEIGHT, vWidth, vHeight)
            Settings.setWidth( vWidth )
            Settings.setHeight( vHeight )
            vScreenDimensions = (Settings.WIDTH, Settings.HEIGHT)
            aGame.screenRegionConfig(vScreenDimensions, Settings.DISPLAY_SETTING)

        if vEvent.type == pg.KEYDOWN:
            aGame.mGUI.keyDown(vEvent.key)

            if vEvent.key == pg.K_F4 and vAltHeld:
                aGame.quit()

            if aGame.mGameState in INGAMESTATES :
                if regKeybindingDict.get(vEvent.key, None) == EventActions.EndTurn:

                    if aGame.mVerbosity >= 1:
                        print('Ending turn for player %d' % aGame.mCurrentPlayerTurn)
                    aGame.nextTurn()

            if regKeybindingDict.get( vEvent.key, None ) == EventActions.SaveGame:
                aGame.saveGame(1)
            if regKeybindingDict.get( vEvent.key, None ) == EventActions.LoadGame:
                aGame.loadGame()

            if ( regKeybindingDict.get( vEvent.key, None ) == EventActions.OpenConsole ):
                aGame.inConsoleSkipFrame = console.takeInput( aGame )
        # this code is gross and I hate it but im too lazy to clean it up
        # it's a debug thing anyway so im not too concerned
        if aGame.inConsoleSkipFrame:
            aGame.inConsoleSkipFrame = console.takeInput( aGame )

        if vEvent.type == pg.KEYUP:
            aGame.mGUI.keyUp(vEvent.key)

        if vEvent.type == pg.MOUSEMOTION:
            # for vTile in aGame.mAllTerrainGroup:
            #     vMouseX, vMouseY = vEvent.pos
            #     vDisplacedX = vMouseX + aGame.mCamera.xShift
            #     vDisplacedY = vMouseY + aGame.mCamera.yShift
            #     if vTile.rect.collidepoint(vDisplacedX, vDisplacedY):
            #         vFoundTile = True
            #         aGame.mSelector.mTile = vTile
            #         aGame.mSelector.moveSelector()
            # # if no tile is found it means cursor is off the map
            # if vFoundTile == False:
            #     aGame.mSelector.mTile = None
            #     aGame.mSelector.moveSelector()
            pass

        if vEvent.type == pg.MOUSEBUTTONDOWN:
            aGame.mGUI.mouseDown(pg.mouse.get_pos())


            if aGame.mGameState in INGAMESTATES:
                if vEvent.button in regKeybindingDict.keys():
                    vTile = aGame.mSelector.mTile
                    if vTile != None:
                        vTile.eventHandle(regKeybindingDict[vEvent.button])

                vDeltaXFromScreen, vDeltaYFromScreen = pg.mouse.get_pos()
                if aGame.mCamera :

                    vMouseXRelativePos = vDeltaXFromScreen - aGame.mCamera.xShift
                    vMouseYRelativePos = vDeltaYFromScreen - aGame.mCamera.yShift

                    aGame.mZoomChanged = 0

                if regKeybindingDict[vEvent.button] == EventActions.ZoomIn:
                    if aGame.mCamera.mZoomFactor < 1.7:
                        aGame.mCamera.mZoomChange = 1 + (0.1 / aGame.mCamera.mZoomFactor)
                        aGame.mCamera.mZoomFactor += 0.1
                        aGame.mZoomChanged = 1

                if regKeybindingDict[vEvent.button] == EventActions.ZoomOut:
                    if aGame.mCamera.mZoomFactor > 1 :
                        aGame.mCamera.mZoomChange = 1 - (0.1 / aGame.mCamera.mZoomFactor)
                        aGame.mCamera.mZoomFactor -= 0.1
                        aGame.mZoomChanged = 1

        if vEvent.type == pg.MOUSEBUTTONUP:
            aGame.mGUI.mouseUp(pg.mouse.get_pos())