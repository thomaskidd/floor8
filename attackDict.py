# Copyright © 2018 This material is the property of the individuals that contributed to it: Dennis Vidovic, Andrew Rae, Thomas Kidd and Yusef Zia.
# It may NOT be copied or otherwise used, in part or in its entirety, without permission, for any purpose, other than to execute it on a computing
# platform as a complete project, without modifications.

# dict containing attack efficacy against other unit elavations
import settings as s
gAttackDict = {
    'LightInfantry' : {
        s.WhereThouDothReside.HIGHAIR : None,
        s.WhereThouDothReside.LOWAIR : 0.5,
        s.WhereThouDothReside.GROUND : 1.,
        s.WhereThouDothReside.WATER : 0.5,
        s.WhereThouDothReside.SUBMERGED : None,
    },
    'Battleship': {
        s.WhereThouDothReside.HIGHAIR: 0.9,
        s.WhereThouDothReside.LOWAIR: 1.,
        s.WhereThouDothReside.GROUND: 1.,
        s.WhereThouDothReside.WATER: 1.,
        s.WhereThouDothReside.SUBMERGED: 0.75,
    },
}