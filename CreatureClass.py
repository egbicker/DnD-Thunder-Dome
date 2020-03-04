import math
import json

import pdb
class Creature:

    def __init__(self, input_file = None):
        
        #Required Inputs:
        # - Name, string
        
        #Optional Inputs:
        #- size: string. Default to Medium
        #    - tiny, small, medium, large, huge, gargantuan
        #- stock: string. Default to humanoid
        #    - abberation, beast, celestial, construct, dragon, elemental, fey,
        #    - fiend, giant, humanoid, monstrosity, ooze, plant, swarm, undead
        #- alignment: string. Default to N
        #   - LG, NG, CG, LN, N, CN, LE, NE, CE
        #- initiative_modifier: int, Defaults to DEX mod if not specified
        #- armor_class: int, Defaults to 10 if not specified
        #- hit_points: dict
        #    - method: string, Defaulsts to 'Exact'
        #       - Exact: Known and invariant (PC's), ignores hit dice 
        #       - Average: Average of hit dice listed (monsters that have ndX hit dice)
        #       - Normal: Take statistical draws on a given formula (monsters that have ndX hit dice)        
        #    - value: string or int, Defaults to 1
        #       - Exact: int, number of hp
        #       - Average: string, hp code (ndY + X) where n is num hit die, Y is hit die type, X is flat
        #       - Normal: string, hp code (ndY + X) where n is num hit die, Y is hit die type, X is flat
        #- movement: dict. All units in ft
        #    - land: int, defaults to 30
        #    - swim: int, defaults to 0
        #    - fly: int, defaults to 0
        #    - climb: int, defaults to 0
        #    - burrow: int, defaults to 0
        #- att_scores: dict. The raw score, not the modifier
        #    - strength: int, defaults to 10
        #    - dexterity: int, defaults to 10
        #    - constitution: int, defaults to 10
        #    - intelligence: int, defaults to 10
        #    - wisdom: int, defaults to 10        
        #    - charisma: int, defaults to 10        
        #- save_mod: dict. Represents the TOTAL saving throw modifier
        #    - strength: int, defaults to modifier
        #    - dexterity: int, defaults to modifier
        #    - constitution: int, defaults to modifier
        #    - intelligence: int, defaults to modifier
        #    - wisdom: int, defaults to modifier       
        #    - charisma: int, defaults to modifier   
        #- skills: Not Yet Implemented
        #TODO: Skills
        
        self.creature = dict(
                
                        #The creature's name
                        #TODO: Break if the name is empty
                        #TODO: Deal with uniquness in naming (the 17 kobold load problem)
                        name = [],
                        
                        size = 'medium',
                        
                        stock = 'humanoid',
                        
                        alignment = 'N',
                        
                        #Initiative modifier
                        #Default to empty, default to dex-mod if not input 
                        initiative_modifier = [],
         
                        #Armor Class. Defaults to 10
                        armor_class = 10,
            
                        #Hit Points
                        hit_points = dict( 
                                            method = 'Exact',
                                            value = 1),

                        #Movement types: land, swim, fly, climb, burrow
                        #Initialize with 30 feet of normal movement only
                        movement = dict (
                                            land   = 30,
                                            swim   = 0,
                                            fly    = 0,
                                            climb  = 0,
                                            burrow = 0),


                        # Initialize all attributes to 10
                        att_scores = dict(
                                            strength     = 10,
                                            dexterity    = 10,
                                            constitution = 10,
                                            intelligence = 10,
                                            wisdom       = 10,
                                            charisma     = 10),

                        #Initialize all ability modifiers as empty
                        #Just in case we want to only specify modifiers later????
                        #After input, we will calculate the modifiers with Creature::score2modifier()
                        att_mods = dict(
                                             strength     = [],
                                             dexterity    = [],
                                             constitution = [],
                                             intelligence = [],
                                             wisdom       = [],
                                             charisma     = []),

                        #Initialize all saving throw bonuses to empty
                        #Assume the user input value is the total save
                        #If a value is empty (not a number) then default it to the same as att_mods
                        save_mod = dict(
                                          strength     = [],
                                          dexterity    = [],
                                          constitution = [],
                                          intelligence = [],
                                          wisdom       = [],
                                          charisma     = []),

                        #Damage types
                        #A give creature can be Immune, Resistant, Neutral or Vulnerable
                        #Since these are mutually exclusive, I'm categorizing by damage type
                        #Instead of by the 4 types with all damage listed under each
                
                        #Initialize all damage types to 1 (Neutral)
                        damage = dict(
                                           acid        = 1,
                                           bludgeoning_m  = 1,
                                           bludgeoning_nm = 1,
                                           cold        = 1,
                                           fire        = 1,
                                           force       = 1,
                                           lightning   = 1,
                                           necrotic    = 1,
                                           piercing_m    = 1,
                                           piercing_nm   = 1,
                                           poison      = 1,
                                           psychic     = 1, 
                                           radiant     = 1,
                                           slashing_m    = 1,
                                           slashing_nm   = 1,
                                           thunder     = 1),



                        #Current Condition Status
                        condition_status = dict(
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
                        )
                        
        self.exhaustion_level = 0
        self.is_surprised = False
        
        if input_file:
            self.parseInputFile(input_file)
        
    def parseInputFile(self,input_file):
        try:
            with open(input_file, 'r') as f:
                creature_data = json.load(f)
                f.close
                
            for key in creature_data.keys():
                if key in self.creature.keys():
                    if isinstance(self.creature[key],dict):
                        self.creature[key].update(creature_data[key])
                    else:
                        self.creature[key] = creature_data[key]

                else:
                    print(key + ' is not a valid input name')
    
                
                                
        except FileNotFoundError as fnf_error:
            print(fnf_error)
    
    def score2modifier(abilityScore):

        #use floor() for proper handling of negative modifiers
        #The equation is (score - 10)/2 round down
        modifier = math.floor( (abilityScore - 10)/2 )

        return modifier

    def level2proficiency(level):

        #Equation is level/4 + 1 rounded up
        proficency = math.ceil( level/4 ) + 1

        return proficiency