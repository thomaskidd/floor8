from spritesList import *

movementDicts = {
    'LightInfantry': {
        TerrainTypes.waterTile: None,
        TerrainTypes.grassTile: 1.,
        TerrainTypes.plainTile: 1.,
        TerrainTypes.mountainTile: 2.,
        TerrainTypes.forestTile: 1.,
        TerrainTypes.cityTile: 1.,
    },
    'Battleship': {
        TerrainTypes.waterTile: 1.,
        TerrainTypes.grassTile: None,
        TerrainTypes.plainTile: None,
        TerrainTypes.mountainTile: None,
        TerrainTypes.forestTile: None,
        TerrainTypes.cityTile: None,
    }
}