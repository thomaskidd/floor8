# parent class for all menus

from enum import Enum
from settings import Settings
from label import Label
from button import Button

class Position(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4

class Menu:

    def __init__( self ):
        # arrays of active components and buttons
        self.mComponents = []
        self.mButtons = []

        # array of containers, each container holds one menu
        self.mContainers = []

        # positioning variables
        self.mNumItems = 5
        self.mComponentWidth = Settings.WIDTH / 3.2     # 400 px
        self.mComponentHeight = Settings.HEIGHT / 10    # 80 px
        self.mComponentXPos = Settings.WIDTH / 2 - self.mComponentWidth / 2
        self.mComponentYPos = Settings.HEIGHT / 2 - (self.mComponentHeight * self.mNumItems / 2)
        self.mFontSize = Settings.WIDTH / 42.67         # size 30
        self.mPadding = 10

    # add components
    def addLabel( self, aText, aPos ):
        self.mComponents.append(Label(self.mComponentXPos, self.mComponentYPos + (self.mComponentHeight + self.mPadding) * aPos, self.mComponentWidth, self.mComponentHeight, aText))
        self.mComponents[-1].setFontSize(self.mFontSize)

    def addButton( self, aText, aCommand, aPos ):
        self.mComponents.append(Button(self.mComponentXPos, self.mComponentYPos + (self.mComponentHeight + self.mPadding) * aPos, self.mComponentWidth, self.mComponentHeight, aText, aCommand))
        self.mButtons.append(self.mComponents[-1])
        self.mComponents[-1].setFontSize(self.mFontSize)

    def addTextField( self, aPos ):
        raise NotImplementedError("This has not been implemented.")

    # add a custom set of components
    def addComponents( self, aComponents):
        for component in aComponents:
            self.mComponents.append(component)
            if type(component) is Button:
                self.mButtons.append(component)

    # add a sub menu
    def addContainer( self, aContainer ):
        self.mContainers.append(aContainer)

    # drawing
    def drawAll( self, aScreen ):
        # draw components in reverse so the component on top is what the user clicks on
        for i in range(len(self.mContainers)-1, -1, -1):
            self.mContainers[i].drawAll(aScreen)

        for i in range(len(self.mComponents)-1, -1, -1):
            self.mComponents[i].draw(aScreen)

    def setPositioning( self, aNumItems, aComponentWidth, aComponentHeight, aHorizontalPos, aVeritcalPos ):
        self.mNumItems = aNumItems
        self.mComponentWidth = aComponentWidth
        self.mComponentHeight = aComponentHeight

        # vertical positioning
        if aVeritcalPos == Position.TOP:
            self.mComponentYPos = self.mPadding
        elif aVeritcalPos == Position.BOTTOM:
            self.mComponentYPos = Settings.HEIGHT - ((self.mComponentHeight + self.mPadding) * self.mNumItems)
        else: # center is default
            self.mComponentYPos = Settings.HEIGHT / 2 - (self.mComponentHeight * self.mNumItems / 2)

        # horizontal positioning
        if aHorizontalPos == Position.LEFT:
            self.mComponentXPos = self.mPadding
        elif aHorizontalPos == Position.RIGHT:
            self.mComponentXPos = Settings.WIDTH - self.mComponentWidth
        else: # center is default
            self.mComponentXPos = Settings.WIDTH / 2 - self.mComponentWidth / 2

    # event handling
    def mouseDown( self, aMousePos ):
        for button in self.mButtons:
            # allow only one button to be clicked
            if button.mouseDown(aMousePos):
                break

        for container in self.mContainers:
            container.mouseDown(aMousePos)

    def mouseUp( self, aMousePos ):
        for button in self.mButtons:
            button.mouseUp(aMousePos)

        for container in self.mContainers:
            container.mouseUp(aMousePos)

    def keyDown( self, aKey ):
        for container in self.mContainers:
            container.keyDown(aKey)

    def keyUp( self, aKey ):
        for container in self.mContainers:
            container.keyUp(aKey)

    def resizeComponents( self, aOldWidth, aOldHeight, aNewWidth, aNewHeight ):

        for component in self.mComponents:
            vPos = component.getLocation()
            vSize = component.getRealSize()

            vXRatio = vPos[0]/aOldWidth
            vYRatio = vPos[1]/aOldHeight
            vWidthRatio = vSize[0]/aOldWidth
            vHeightRatio = vSize[1]/aOldHeight
            vFontRatio = component.getFontSize()/aOldWidth

            component.setLocation(vXRatio*aNewWidth, vYRatio*aNewHeight)
            component.setSize(vWidthRatio*aNewWidth, vHeightRatio*aNewHeight)
            component.setFontSize(vFontRatio*aNewWidth)

        for container in self.mContainers:
            container.resizeComponents(aOldWidth, aOldHeight, aNewWidth, aNewHeight)

    # getters and setters
    def getComponentXPos( self ):
        return self.mComponentXPos

    def getComponentYPos( self ):
        return self.mComponentYPos

    def getComponentWidth( self ):
        return self.mComponentWidth

    def getComponentHeight( self ):
        return self.mComponentHeight

    def getComponentPadding( self ):
        return self.mPadding

    def setVisibleToggle( self, bool ):
        for component in self.mComponents:
            component.setVisibleToggle(False)

    def setParent( self, aParent ):
        self.mParent = aParent

    def getParent( self ):
        return self.mParent

    def setPadding( self, aPadding ):
        self.mPadding = aPadding

    def getPadding( self ):
        return self.mPadding