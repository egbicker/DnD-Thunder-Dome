# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 18:08:00 2020

@author: Elliot
"""
import random

   
def roll_dice(n_dice, n_sides):
    
    results = []
    
    for dice in range(n_dice):
        results.append(random.randint(1,n_sides))

    return (sum(results),results)

#Roll a d20
def d20_roll():
    return roll_dice(1,20)[0]

def evaluate_dice_string(dice_string):
    split_string = dice_string.strip().split('+')
    
    return_list = split_string[0].split('d')
    return_list.append(split_string[-1])
    
    return [int(val) for val in return_list]