import os
import json
from sympy import Symbol, solve

synonymTable = {
    "Mass": "m",
    "mass": "m",
    "M": "m",
    "m": 'm',
    "Time": "t",
    "time": "t",
    "T": "t",
    "t": "t",
    "Acceleration": "a",
    "acceleration": "a",
    "A": "a",
    "a": "a",
    "Velocity": "v",
    "velocity": "v",
    "V": "v",
    "v": "v",
    "Distance": "d",
    "distance": "d",
    "Displacement": "d",
    "displacement": "d",
    "d": "d",
    "D": "d"
}

equationTable = {
    "v * t + 0.5 * a * t ** 2 - d": ["v", "t", "a", "d"]
}



def convertTokens(vars):
    #iterate through vars
    #   search string in synonym table
    #   Replace with value

    for key in vars:
        if key in synonymTable:
            vars[synonymTable[key]] = vars.pop(key)
        else:
            print(key, " was not found.")

    return vars

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def displayMenu():
    print("####################################")
    print("Welcome to PanaCalc v0.2")
    print("Here's a list of commands:")
    print("exit - terminate program")
    print("show - show inputted variables")
    print("calc - solve equations if possible")

def tryEquations(userVars):

    for eq in equationTable:
        if len(intersection(equationTable[eq], list(userVars.keys()))) == len(equationTable[eq]) - 1:        #Doable calculation found
            solveString = eq
            for key2 in userVars:           #Replace variables with values in equation
                solveString = solveString.replace(key2, str(userVars[key2]))

            #print (intersection(equationTable[eq], list(userVars.keys())))
            solveVar = [x for x in equationTable[eq] if x not in list(userVars.keys())]
            solveVar = solveVar[0]

            print("Solving for ", solveVar)
            x = Symbol(solveVar)

            print("A holy answer has been found!")
            print(solveVar, " = ", solve(solveString, solveVar))









    #Iterate through equations
    #   Check if all but one required Vars is filled
    #   If so, copy equation string
    #   Replace symbols with values
    #   solve and output



#################
############# Main
#################

done = False
userVars = {
    "mass": 5,
    "t": 2,
    "acceleration": 3,
    "D": 7
}

while (not done):
    displayMenu()
    userInput = input()

    userVars = convertTokens(userVars)
    if userInput == "exit":
        done = True
        break
    if userInput == "show":
        print(userVars)
    if userInput == "calc":
        if len(userVars) == 0:
            print("No variables detected.")
        tryEquations(userVars)


json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
parsed_json = json.loads(json_string)
print(parsed_json['first_name'])
























