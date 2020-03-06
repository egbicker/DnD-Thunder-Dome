# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 20:27:13 2020

@author: Elliot
"""

from BattleManager import BattleManager

BM = BattleManager()

BM.addCreature("tiamat.json")

print(BM.creatureList)