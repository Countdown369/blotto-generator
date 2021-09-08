#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:56:38 2021

@author: Connor Brown, cabrown802@gmail.com

"""
# IMPORTS
import numpy as np
import random
import ast

# GLOBAL VARIABLES

FILENAME = 'savedTurnsTextFile.txt'

#FUNCTIONS
#----------------------------------------------------------------------------
# Used to tell if a castle's number is "Big" for constructing Smart inputs.

def isBig(num):
    
    if num > 28:
        return True
    else:
        return False
#----------------------------------------------------------------------------
# Used to tell if a castle's number is "Small" for constructing Smart inputs.

def isSmall(num):
    
    if num > 0 and num < 4:
        return True
    else:
        return False
#----------------------------------------------------------------------------
# Creates the first part of a Smart input: makes three Big moves in a row,
# with these castles being either the first 3, second 3, or third 3.

def smart_input_triple():
    
    # List to eventually return
    
    a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    # List of numbers to choose from to put in the list
    
    bigNums = [29, 30, 31, 32, 33, 34, 35, 36, 37]
    
    # Generate a random number 0-2 to choose if it's the first or second or
    # third 3 castles which get stacked
    
    randNum = random.randrange(3)
    
    if randNum == 0:
        for index in range(0, 3):
            a[index] = random.choice(bigNums)
    if randNum == 1:
        for index in range(1, 4):
            a[index] = random.choice(bigNums)
    if randNum == 2:
        for index in range(2, 5):
            a[index] = random.choice(bigNums)
            
    # If it chooses numbers which use more soliders than we have, redo.
    
    if sum(a) > 100:
        
        while(sum(a) > 100):
            
            if randNum == 0:
                for index in range(0, 3):
                    a[index] = random.choice(bigNums)
            if randNum == 1:
                for index in range(1, 4):
                    a[index] = random.choice(bigNums)
            if randNum == 2:
                for index in range(2, 5):
                    a[index] = random.choice(bigNums)
    return a
#----------------------------------------------------------------------------
# Returns Smart input by generating the big numbers first and then filling
# in small numbers into empty castles.
def return_smart_input():
    
    # Creates a list of all zeroes except for a leading sequence of 3 big nums
    
    a = smart_input_triple()
    
    # If that list is already at sum = 100, return it as a Smart input
    
    if sum(a) == 100:   
        return a
    
    # Otherwise, add small numbers to relevant 'zero' spaces until sum = 100
    else:
        
        smallNums = [1, 2, 3]
        
        sumCounter = 0
        
        while (sum(a) != 100):
            
            if sumCounter > 200:
                return a
            
            if (isBig(a[0]) and isBig(a[1]) and isBig(a[2])):
                index = random.choice([3, 4, 5])
                if isSmall(a[index]):
                    pass
                else:
                    a[index] = random.choice(smallNums)
                    if sum(a) > 100:
                        a[index] = 0
                    
            if (isBig(a[1]) and isBig(a[2]) and isBig(a[3])):
                index = random.choice([0, 4, 5, 6])
                if isSmall(a[index]):
                    pass
                else:
                    a[index] = random.choice(smallNums)
                    if sum(a) > 100:
                        a[index] = 0
                    
            if (isBig(a[2]) and isBig(a[3]) and isBig(a[4])):
                index = random.choice([0, 1, 5, 6, 7])
                if isSmall(a[index]):
                    pass
                else:
                    a[index] = random.choice(smallNums)
                    if sum(a) > 100:
                        a[index] = 0
            
            sumCounter += 1
            
    return a
#----------------------------------------------------------------------------

# Return an input of random numbers.

def return_random_input():
    
    # Create a list of 10 random numbers that sum to 100

    a = np.random.random(10)
    a /= a.sum()
    a *= 100
    
    # Round nums to nearest int
    
    a = np.rint(a)
    
    # If last operation makes sum != 100, fix it randomly
    
    while sum(a) != 100.0:
        if sum(a) > 100.0:
            X1 = np.random.randint(low=0, high=10)
            a[X1] -= 1
        if sum(a) < 100.0:
            X1 = np.random.randint(low=0, high=10)
            a[X1] += 1
        
    return a
#----------------------------------------------------------------------------
# Returns a random input sorted in descending order

def return_opening_input():
    
    a = return_random_input()
    
    return -np.sort(-a)
#----------------------------------------------------------------------------
# Returns a random input sorted in ascending order

def return_endgame_input():
    
    a = return_random_input()
    
    return np.sort(a)
#----------------------------------------------------------------------------
# Probabalistically returns a relevant turn for myTurn to be

def return_myTurn_dist():
    
    randInt = random.randrange(1000)
    
    if randInt < 1:
        return return_endgame_input()
    elif randInt <= 10:
        return return_opening_input()
    elif randInt <= 460:
        return return_random_input()
    else:
        return return_smart_input()
#----------------------------------------------------------------------------
# Plays a game of Blotto with two lists of 10 numbers that sum to 100.

def thegame(myTurn, enemyTurn):
    
    # Setup points and "counter" to count 3 in a row
    myPoints = 0
    enemyPoints = 0
    myCounter = 0
    enemyCounter = 0
    
    # For each castle
    
    for index in range(10):
        
        # If I win that castle
        
        if myTurn[index] > enemyTurn[index]:
            
            # Give me points,
            
            myPoints += index
            
            # notch my counter, reset the enemies counter,
            
            myCounter += 1
            if enemyCounter > 0:
                enemyCounter = 0
                
            # if I got 3 in a row, give me more points.
            
            if myCounter == 3:
                for points in range((index+1), 10):
                    myPoints += points
                    
        # If the enemy wins, perform the above operations backwards
        
        elif myTurn[index] < enemyTurn[index]:
            
            enemyPoints += index
            enemyCounter += 1
            
            if myCounter > 0:
                myCounter = 0
                
            if enemyCounter == 3:
                for points in range((index+1), 10):
                    enemyPoints += points
                    
        # If there's a tie, just reset the counters.
        
        else:
            
            myCounter = 0
            enemyCounter = 0
    
    # Return the scoreboard
    
    return myPoints, enemyPoints
#----------------------------------------------------------------------------
# Produces a list of "strong" inputs; creates inputs with
# return_myTurn_dist(), then tests them against many inputs of all kinds.
# Inputs with a strong enough win / loss ratio are saved.

# Will test as many inputs for strength as is indicated by positional argument.

def produceSavedTurns(numTurns):
    
    savedTurns = []
    
    for p in range(numTurns):
        
        myTurn = return_myTurn_dist()
    
        games = []
        wins = 0
        losses = 0
        
        # Creates 2000 inputs to test myTurn against.
        
        for i in range(2000):
            
            if (i < 10):
                enemyTurn = return_endgame_input()
            elif (i < 50):
                enemyTurn = return_opening_input()
            elif (i < 550):
                enemyTurn = return_random_input()
            else:
                enemyTurn = return_smart_input()
            
            # Runs the game with these two inputs.
            
            myPoints, enemyPoints = thegame(myTurn, enemyTurn)
            
            # Handles wins, losses, and ties.
            
            if myPoints > enemyPoints:
                game = str("W " + str(myPoints) + " " + str(enemyPoints))
                games.append(game)
                wins += 1
            elif myPoints < enemyPoints:
                game = str("L " + str(myPoints) + " " + str(enemyPoints))
                games.append(game)
                losses += 1
            else:
                game = str("T " + str(myPoints) + " " + str(enemyPoints))
                games.append(game)
                
        # Save myTurn if it has enough success
        
        if wins / losses > 2:
            savedTurns.append(myTurn)
        
        # Print progress so you don't go crazy while your computer calculates
        # the results of hundreds of millions of Blotto games
        
        print(p)
        
    # Optionally, save savedTurns to a file.
    
    # f = open(FILENAME, "w")
    # f.write(str(savedTurns))
    
    return savedTurns
#----------------------------------------------------------------------------
# Returns the strongest half (approxiamtely) of Blotto inputs from a list
# given as an  argument by playing every input against every other input.

def tournament(savedTurns):
    
    savedWinners = []
    i = 0
    
    for turn in savedTurns:
        
        print(i)
        
        myTurn = turn
        
        wins = 0
        losses = 0
        
        for enemyTurn in savedTurns:
            
            myPoints, enemyPoints = thegame(myTurn, enemyTurn)
            
            if myPoints > enemyPoints:
                wins += 1
            elif myPoints < enemyPoints:
                losses += 1
                
        if losses == 0 or wins >= losses:
            savedWinners.append(myTurn)
            
        i += 1
    
    
    return savedWinners
#----------------------------------------------------------------------------
# Run a tournament until only 1 (or, in the worst cases, 2 or 3) input remains.

def ultimateTournament(savedTurns):
    
    # If a list is the same length after it's been tournamized,
    # that might be an issue. Here, we keep track of it.
    
    duel = len(savedTurns)
    
    savedWinners = tournament(savedTurns)
    
    # Handle small numbers of inputs which get stuck fighting each other
    
    if len(savedWinners) > 1:
        if len(savedTurns) == duel:
            if duel < 4:
                return savedWinners
            else:
                savedWinners = ultimateTournament(savedWinners)
        else:
            savedWinners = ultimateTournament(savedWinners)
            
    return savedWinners
#----------------------------------------------------------------------------
def main():
    
    theList = produceSavedTurns(100)
    
    # If your list is saved as a file, use this to read it back in.
    # Make sure the list looks like this in the text file:
    # ['element 1', 'element 2', 'element 3', 'element 4']
    # (I used a non-Python find-and-replace tool to amend my text file)

    # with open(FILENAME, 'r') as f:
    #   mylist = ast.literal_eval(f.read())

    print(ultimateTournament(theList))
    
main()
