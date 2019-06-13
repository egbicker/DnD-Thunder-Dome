# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 16:59:13 2019

@author: Elliot
"""

import json
import random

#Roll a d20
def d20Roll():
    return random.randint(1,20)
    
#This class handles scheduling and adding/removing monsters
class BattleManager :
    
    #Maximum initiative to count down from. This could be higher but 40 seems reasonable
    maxInitiative = 40
    
    def __init__ (self):
        
        #init the creatures in the fight to empty when creating a new battle
        self.creatureList = []
        self.conditionStatus = dict(
                               blinded       = False,
                               charmed       = False,
                               deafened      = False,
                               frightened    = False,
                               grappled      = False,
                               incapacitated = False,
                               invisible     = False,
                               paralyzed     = False,
                               petrified     = False,
                               poisoned      = False,
                               prone         = False,
                               restrained    = False,
                               stunned       = False,
                               unconcious    = False)
        
        self.exhaustionLevel = 0
        self.isSurprised = False
        
    #Call this for each file containing a single creature
    #TODO: Make this accept multiple of the same file and then unique-ify them
    #TODO: Even later, accept multiple of the same creature and then randomize their HP/abilities...     
    def addCreature(self, inputFile):

        try:
            with open(inputFile, 'r') as f:
                newCreature = json.load(f)
                f.close
                                        
            #TODO: If no initiative modifier, use dex mod. If no dex mod, set warning and set mod to 0 or throw error?    
            #TODO: Add the ability to set initative in the json. This means checking to see if the field already exists, if not calculate it randomly
            #TODO: Sort ties by dexterity ability, if that's a tie, then ???
            
            initRoll = d20Roll()
            newCreature["initiative"] = initRoll + int(newCreature["initiativeModifier"])
            print(newCreature["name"] + " rolled a " + str(initRoll) + " for its initiative resulting in a total of: " + str(newCreature["initiative"]))
            
            
            self.creatureList.append(newCreature)
            
            self.creatureList = sorted(self.creatureList, key = lambda i: i["initiative"], reverse=True)
            
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            
BM = BattleManager()

BM.addCreature("test.json")
BM.addCreature("tiamat.json")

print(BM.creatureList)