import os
import requests
import urllib
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

sinWebsite = 'http://omnicalc.alegemaate.com/api/get_synonyms.php?value='
eqWebsite = 'http://omnicalc.alegemaate.com/api/get_equations.php?tokens='
seperator = '-'

def convertTokens(vars):
    for key in vars:
        r = requests.get(sinWebsite + str(key))        #Get key from api
        #print(website + str(key))
        #print(r.text)

        jsonFriendlyString = r.text.replace("'", "\"")               #Convert to json
        temp = json.loads(jsonFriendlyString)

        if temp != []:                         #Converts to dict
            temp = temp[0]
            token = temp["token"]              #We got a token
            vars[token] = vars.pop(key)
        else:
            print(key, " was not found")

    return vars


def displayMenu():
    print("####################################")
    print("Welcome to PanaCalc v0.2")
    print("Here's a list of commands:")
    print("exit - terminate program")
    print("show - show inputted variables")
    print("calc - solve equations if possible")

def parseJSON(jsonData):
    newDict = json.loads(jsonData)

    for key in newDict:
        newDict[key.strip()] = newDict.pop(key).strip()

    return newDict



def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def tryEquations(userVars):
    webString = eqWebsite

    for varKey in userVars:
        webString = webString + str(varKey) + seperator
    webString = webString[:-1]

    r = requests.get(webString)
    jsonFriendlyString = r.text.replace("'", "\"")  # Convert to json
    solvableEqs = json.loads(jsonFriendlyString)

    if solvableEqs != []:
        for eq in solvableEqs:
            solveString = eq["formula"]
            for key in userVars:           #Replace variables with values in equation
                solveString = solveString.replace(key, str(userVars[key]))

            solveVar = [x for x in equationTable[eq] if x not in list(userVars.keys())]
            solveVar = solveVar[0]

            print("Solving for ", solveVar)
            x = Symbol(solveVar)

            print("A holy answer has been found!")
            print(solveVar, " = ", solve(solveString, solveVar))
    else:
        print("No solvable equations")


#    for eq in equationTable:
#        if len(intersection(equationTable[eq], list(userVars.keys()))) == len(equationTable[eq]) - 1:        #Doable calculation found
#            solveString = eq
#            for key2 in userVars:           #Replace variables with values in equation
#                solveString = solveString.replace(key2, str(userVars[key2]))
#
#            #print (intersection(equationTable[eq], list(userVars.keys())))
#            solveVar = [x for x in equationTable[eq] if x not in list(userVars.keys())]
#            solveVar = solveVar[0]
#
#            print("Solving for ", solveVar)
#            x = Symbol(solveVar)
#
#            print("A holy answer has been found!")
#            print(solveVar, " = ", solve(solveString, solveVar))









    #Iterate through equations
    #   Check if all but one required Vars is filled
    #   If so, copy equation string
    #   Replace symbols with values
    #   solve and output



#################
############# Main
#################

userVars = {
    "mass": 5,
    "t": 2,
    "Acceleration": 3,
    "D": 7
}
done = False
data = {}


while (not done):
    displayMenu()
    userInput = input()

    #userVars = parseJSON(jsonData)

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




















