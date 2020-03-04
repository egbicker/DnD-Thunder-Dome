# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 12:13:56 2019

@author: Elliot
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#File that has all the monster info. 
#TODO: Conver to csv? 
mm_file = 'D:\Modron Fight Club\Monster_Manual.xlsx'

#Read in the whole sheet that has all relevant info
mm_df = pd.read_excel(mm_file, 
                      header = 0,
                      sheet_name='Monsters'
                      )

#Remake the DF to only have the columns the user cares about
#This list can be adjusted by the user or whatever they want to do
mm_df = mm_df[['Name',
                'Size',
                'CR',
                'AC',
                'HP',
                'STR MOD',
                'DEX MOD',
                'CON MOD',
                'INT MOD',
                'WIS MOD',
                'CHA MOD',
                'STR SAVE',
                'DEX SAVE',
                'CON SAVE',
                'INT SAVE',
                'WIS SAVE',
                'CHA SAVE',
                'Bludgeoning',
                'Piercing',
                'Slashing',	
                'Acid',	
                'Cold',	
                'Fire',	
                'Force',	
                'Lightning',	
                'Necrotic',	
                'Poison',	
                'Psychic',	
                'Radiant',	
                'Thunder',	
                'Blinded',	
                'Charmed',	
                'Deafened',	
                'Exhaustion',	
                'Frightened',	
                'Grappled',	
                'Paralyzed',	
                'Petrified',
                'Poisoned',
                'Prone',	
                'Restrained',	
                'Stunned',	
                'Unconscious'
                ]
             ]



#Assumes blank cells should be treated as 0's
#TODO: Save off .csv file with empty spots as 0's to remove this line
mm_df = mm_df.fillna(0)

#TODO One-hot encode damage vulnerability/resistance/immunity


#Remove Name and Size since I don't care
mm_name = mm_df.pop('Name')
mm_size = mm_df.pop('Size')



#plt.yticks(np.arange(1,26))
#Convert Stat values to modifiers, which is what actually matters

#Attribut to modifier: divide by 2, round down - 5

