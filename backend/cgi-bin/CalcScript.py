#!/usr/bin/env python

import cgi;
import cgitb
cgitb.enable()

import requests
import json
import unicodedata
from sympy import Symbol, solve

sinWebsite = 'http://omnicalc.alegemaate.com/api/get_synonyms.php?value='
eqWebsite = 'http://omnicalc.alegemaate.com/api/get_equations.php?tokens='
seperator = '-'

def print_header():
    print ("""Content-type: text/html\n""")

def print_close():
    print ("""""")

def display_data(data):
    print_header()
    print ("<p>" + data + "</p>")
    print_close()

def display_error():
    print_header()
    print ("<p>An Error occurred parsing the parameters passed to this script.</p>")
    print_close()


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

def parseJSON(jsonData):
    try:
        newDict = json.loads(jsonData)
    except:
        return {}
    for key in newDict:
        newDict[key.strip()] = newDict.pop(key)
     
    return newDict



def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def tryEquations(userVars):
    returnString = ""
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
            returnString = str(eq["formula"])
            for key in userVars:           #Replace variables with values in equation
                solveString = solveString.replace(key, str(userVars[key]))


            solveVar = [x for x in eq['formula'] if x not in list(userVars.keys())]

            x = ''
            for z in solveVar:
              if z.isalpha():
                x = Symbol(z)

            returnString = returnString + "<br>" + str(x) + " = " + str(solve(solveString, x))
    else:
        returnString = "No solvable equations"
        
    return returnString


####################################
############### Main ###############
####################################

def main():
  data = {}

  form = cgi.FieldStorage()

  if (form.has_key("param1")):      
      userVars = parseJSON(form["param1"].value)
      if userVars != {}:
        #userVars = convertTokens(userVars)
        #display_data(str(userVars))
        display_data(tryEquations(userVars))
  else:
      display_error()
      
main()


















