import spritesList

class Player():
    def __init__( self, aGame, aPlayerId, aStartingMoney ):
        self.mGame = aGame
        self.mID = aPlayerId
        self.mMoney = int( aStartingMoney )
        self.mUnits = []

        self.mCitiesOwned = []


        # this is a dictionary of unit bonuses achieved through research
        # and other such ways
        self.mUnitBonuses = {
            # light infantry
            'LightInfantryBonusMove' : 0, # there is flat bonuses

            'LightInfantryAttackDamagePercent' : 1.00, # and also percentage increases
            'LightInfantryAttackDamageFlat' : 0,

            'LightInfantryAPBonusPercent' : 1.00,
            'LightInfantryAPBonusFlat' : 0,

            'LightInfantryHealthBonusPercent' : 1.00,
            'LightInfantryHealthBonusFlat' : 0,

            'LightInfantryArmourBonusPercent' : 1.00,
            'LightInfantryArmourBonusFlat' : 0,

            # Battleship
            'BattleshipBonusMove' : 0, # there is flat bonuses

            'BattleshipAttackDamagePercent' : 1.00, # and also percentage increases
            'BattleshipAttackDamageFlat' : 0,

            'BattleshipAPBonusPercent' : 1.00,
            'BattleshipAPBonusFlat' : 0,

            'BattleshipHealthBonusPercent' : 1.00,
            'BattleshipHealthBonusFlat' : 0,

            'BattleshipArmourBonusPercent' : 1.00,
            'BattleshipArmourBonusFlat' : 0,
        }

    def update(self):
        pass

    def saveHelper( self ):
        vInfo = ( self.mID, self.mMoney )
        return vInfo

# TODO depending on how we do character select, we should have a way of changing these before the game starts
playerIdColourDict ={
    0 : 'Red',
    1 : 'Blue',
}

playerIdCityTypeDict = {
    0 : spritesList.TerrainTypes.redCityTile,
    1 : spritesList.TerrainTypes.blueCityTile,
}