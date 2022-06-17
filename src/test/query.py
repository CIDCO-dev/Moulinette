# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 17:30:28 2022

@author: Hydrograhe
"""
import sys

def query():
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    
    question= "Truncation is weight based (1) or frequency based (2) ? [1/2]"
    
    
    #valid = {"1": True,"weight":True, "2": False, "frequency":False}

    sys.stdout.write(question)
    choice = input().lower()
    if choice == 1:
        return "weight"
    elif choice == 2:
        sys.stdout.write("What was the maximum frequency allowed ?")
        choice = input().lower()
        if type(choice) == int:
            return f"freq_{choice}"
        else :
            sys.stdout.write("Unfited value")
            query()
        
    else:
        sys.stdout.write("Please respond with '1' or '2' " "(or 'weight' or 'frequency').\n")
            