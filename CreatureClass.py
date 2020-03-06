import math
import json
import utils

import pdb
class Creature:

    def __init__(self, input_file = None):
        
        #Required Inputs:
        # - name, string
        
        #Recommended Inputs:
        # - language, list of strings
        #   - This is required in the sense that if you don't specify anything it will remain blank
        #     However, since it is likely not useful, it won't break if you don't
        
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
        #- max_hit_points: dict
        #    - method: string, Defaulsts to 'Exact'
        #       - exact: Known and invariant (PC's), ignores hit dice 
        #       - average: Average of hit dice listed (monsters that have ndX hit dice)
        #       - roll: Take statistical draws on a given formula (monsters that have ndX hit dice)        
        #    - value: string or int, Defaults to 1
        #       - exact: int, number of hp
        #       - average: string, hp code (ndY + X) where n is num hit die, Y is hit die type, X is flat
        #       - roll: string, hp code (ndY + X) where n is num hit die, Y is hit die type, X is flat
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
        #- skills: 
        self.stats = dict(
                
                        #The creature's name
                        #TODO: Break if the name is empty
                        #TODO: Deal with uniquness in naming (the 17 kobold load problem)
                        name = [],
                        
                        size = 'medium',
                        
                        stock = 'humanoid',
                        
                        alignment = 'N',
                        
                        #Initiative modifier
                        #Default to empty, default to dex-mod if not input 
                        initiative_mod = [],
         
                        #Armor Class. Defaults to 10
                        armor_class = 10,
            
                        #Hit Points
                        max_hit_points = dict( 
                                            method = 'exact',
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
                        save_mods = dict(
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
                                           bludgeoning = [1,1],
                                           cold        = 1,
                                           fire        = 1,
                                           force       = 1,
                                           lightning   = 1,
                                           necrotic    = 1,
                                           piercing    = [1,1],
                                           poison      = 1,
                                           psychic     = 1, 
                                           radiant     = 1,
                                           slashing    = [1,1],
                                           thunder     = 1),

                        conditions = dict(
                                           blinded       = 1,
                                           charmed       = 1,
                                           deafened      = 1,
                                           frightened    = 1,
                                           grappled      = 1,
                                           incapacitated = 1,
                                           invisible     = 1,
                                           paralyzed     = 1,
                                           petrified     = 1,
                                           poisoned      = 1,
                                           prone         = 1,
                                           restrained    = 1,
                                           stunned       = 1,
                                           unconcious    = 1),
                        
                        skills = dict(
                                    acrobatics      = [],    
                                    arcana          = [],
                                    animal_handling = [],
                                    athletics       = [],
                                    deception       = [],
                                    history         = [],
                                    insight         = [],
                                    intimidation    = [],
                                    investigation   = [],
                                    medicine        = [],
                                    nature          = [],
                                    perception      = [],
                                    performance     = [],
                                    persuasion      = [],
                                    religion        = [],
                                    sleight_of_hand = [],
                                    stealth         = [],
                                    survival        = []
                                ),
                                
                        #Passive Perception
                        #Default to 10 + Perception (which defaults to Wis)
                        #Not guarunteed to be 10 + Per (e.g. Observant Feat)
                        passive_per = [],
                        
                        #Non-standard senses. Distances in feet
                        senses = dict(
                                    darkvision  = 0,
                                    truesight   = 0,
                                    blindsight  = 0,
                                    tremorsense = 0
                                ),
                                
                                
                        #Languages known
                        #Default to an empty list. If not specified by the user, don't do anything
                        #This is "required" if you want accuracy, but given it's probably useless, who cares?
                        languages = [],

                        #Challenge Rating. Default to 0
                        challenge_rating = 0

                        )

        self.state = dict(
               
            #Current Condition Status
            current_condition = dict(
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
                                   unconcious    = False),
            
            #Current exhaustion level
            #Default to 0
            exhaustion_level = 0,
            
            #Creature surprise boolean
            #Default to False
            is_surprised = False,
            
            #Current total intitiative. Used to determine order
            #Based on roll + self.stats[initiative_modifier]
            initiative = [],
            
            current_hit_points = []
            )
        
        if input_file:
            self.parse_input_file(input_file)
            
            self.calculate_att_mods()
            self.calculate_save_mods()        
            self.calculate_initiative_mod()
            
            self.initialize_hit_points()
            
            self.calculate_skill_mods()
            self.calculate_passive_per()
                    
###############################################################################
                
###############################################################################        
    def parse_input_file(self,input_file):
        try:
            with open(input_file, 'r') as f:
                creature_data = json.load(f)
                f.close  
                                             
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            
        for key in creature_data.keys():
            if key in self.stats.keys():
                if isinstance(self.stats[key],dict):
                    self.stats[key].update(creature_data[key])
                else:
                    self.stats[key] = creature_data[key]

            else:
                print(key + ' is not a valid input name')


###############################################################################
                
###############################################################################
    def score2modifier(self, abilityScore):

        #TODO Sanitize input
        
        #use floor() for proper handling of negative modifiers
        #The equation is (score - 10)/2 round down
        modifier = math.floor( (abilityScore - 10)/2 )

        return modifier
    
###############################################################################
                
###############################################################################        
    def calculate_att_mods(self):
        
        for stat in self.stats["att_mods"].keys():
            if not self.stats["att_mods"][stat]:
                self.stats["att_mods"][stat]=self.score2modifier(self.stats["att_scores"][stat])
                
###############################################################################
                
###############################################################################        
    def initialize_hit_points(self):
        
        if self.stats["max_hit_points"]["method"] == "exact":
            self.state["current_hit_points"] = int(self.stats["max_hit_points"]["value"])
            
        elif self.stats["max_hit_points"]["method"] == "average":
            dice_vals = utils.evaluate_dice_string(self.stats["max_hit_points"]["value"])
            self.state["current_hit_points"] = math.floor(dice_vals[0] * (dice_vals[1] + 1)/2) + dice_vals[2]
            
        elif self.stats["max_hit_points"]["method"] == "roll":
            dice_vals = utils.evaluate_dice_string(self.stats["max_hit_points"]["value"])
            self.state["current_hit_points"] = utils.roll_dice(dice_vals[0],dice_vals[1])[0] + dice_vals[2]
                
###############################################################################
                
###############################################################################        
    def calculate_save_mods(self):
        
        for stat in self.stats["save_mods"].keys():
            if not self.stats["save_mods"][stat]:
                self.stats["save_mods"][stat]=self.stats["att_scores"][stat]
                                        
###############################################################################
                
###############################################################################        
    def calculate_initiative_mod(self):
        
        if not self.stats["initiative_mod"]:
            self.stats["initiative_mod"] = self.stats["att_mods"]["dexterity"]

###############################################################################
                
###############################################################################        
    def calculate_skill_mods(self):

        skill_defaults = dict(
                          strength     = ["athletics"],
                          dexterity    = ["acrobatics","sleight_of_hand","stealth"],
                          intelligence = ["arcana","history","investigation","nature","religion"],
                          wisdom       = ["animal_handling","insight","medicine","perception","survival"],
                          charisma     = ["deception","intimidation","performance","persuasion"]
                          )
        
        for att in skill_defaults.keys():
            for skill in skill_defaults[att]:
                if not self.stats["skills"][skill]:
                   self.stats["skills"][skill] = self.stats["att_mods"][att]
                   
###############################################################################
                
###############################################################################        
    def calculate_passive_per(self):
        
        if not self.stats["passive_per"]:
            self.stats["passive_per"] = self.stats["skills"]["perception"] + 10
###############################################################################
                
###############################################################################
    def level2proficiency(level):

        #Equation is level/4 + 1 rounded up
        proficency = math.ceil( level/4 ) + 1

        return proficiency