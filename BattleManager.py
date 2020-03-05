# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 16:59:13 2019

@author: Elliot
"""

import pdb

import random
from CreatureClass import Creature as cc

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
       
        
    #Call this for each file containing a single creature
    #TODO: Make this accept multiple of the same file and then unique-ify them
    #TODO: Even later, accept multiple of the same creature and then randomize their HP/abilities...     
    def addCreature(self, input_file):

        new_creature = cc(input_file)
        initRoll = d20Roll()
                                                
            #TODO: If no initiative modifier, use dex mod. If no dex mod, set warning and set mod to 0 or throw error?    
            #TODO: Add the ability to set initative in the json. This means checking to see if the field already exists, if not calculate it randomly
            #TODO: Sort ties by dexterity ability, if that's a tie, then ???
            
        new_creature.state["initiative"] = initRoll + new_creature.stats["initiative_modifier"]
#            print(newCreature["name"] + " rolled a " + str(initRoll) + " for its initiative resulting in a total of: " + str(newCreature["initiative"]))
#            
#            
        self.creatureList.append(new_creature)
#            
        self.creatureList = sorted(self.creatureList, key = lambda i: i.state["initiative"], reverse=True)
            

            
BM = BattleManager()

BM.addCreature("tiamat.json")

print(BM.creatureList)