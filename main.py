# -*- coding: utf-8 -*-

import numpy as np
import yaml
import random
import sys
from prettytable import PrettyTable



# Getting input data from data.yaml
def readInput():
    with open("data.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)

            # Parsage des eleves
            students = {}
            studentsCapacities = {}
            
            for student, ranking in data["eleves"].items():
                students[student] = ranking["ecoles"].split()
                studentsCapacities[student] = 1
                #random.shuffle(students[student])
                

            # Parsage des ecoles
            schools = {}
            schoolsCapacities = {}
            for school, ranking in data["ecoles"].items():
                schools[school] = ranking["eleves"].split()
                schoolsCapacities[school] = ranking["capacite"]
                #random.shuffle(students[student])
            
            return students, schools, studentsCapacities, schoolsCapacities
        except yaml.YAMLError as exc:
            print(exc)


# Tous les serenades vont se proposer à leur n seneraded préférés
def serenading(allSerenades, serenadesNotMarried, serenadesCapacities, stableMatch):

    stableChoices = []

    for serenades in serenadesNotMarried:
        # seneraded favori(s) qui ne l'a pas refuse
        for i in range(serenadesCapacities[serenades]):
            # Traiter le cas où capacite > nombre de seneraded restant
            if (i < len(allSerenades[serenades])):
                stableChoices.append(allSerenades[serenades][0])
                allSerenades[serenades].pop(0)

        for stableChoice in stableChoices:
            if stableChoice not in stableMatch:
                stableMatch[stableChoice] = []
            stableMatch[stableChoice].append(serenades)

        # Remettre la liste des choix stable à 0 pour le prochain serenades
        stableChoices.clear()


# Choix de(s) serenade(s) favori parmis la liste de préférence du seneraded
def getStableChoices(serenadesToChoose, ranking, seneradedCapacity):

    stableChoices = []

    for serenades in ranking:
        if serenades in serenadesToChoose:
            stableChoices.append(serenades)
            # Un seneraded ne peut pas choisir plus de serenades que sa capacitié
            if len(stableChoices) >= seneradedCapacity:
                return stableChoices

    return stableChoices

# Retourne une ligne du tableau des stableMatching
def getStableMatchingRow(allseneraded, stableMatch):
    row = []

    for seneraded in allseneraded.keys():
        if seneraded in stableMatch:
            row.append(' '.join(stableMatch[seneraded]))
        else:
            row.append('X')    

    return row

# Afficher les entrées de l'algorithm
def showInput(allSerenades, allseneraded, serenadesCapacities, seneradedCapacities):
    print("Inputs:")

    firstLigne = list(allSerenades.keys())
    firstLigne.insert(0, ' ')
    inputTable = PrettyTable(firstLigne)

    allSerenadesKeys = list(allSerenades.keys())
    allseneradedKeys = list(allseneraded.keys())

    for seneraded, senerades in allseneraded.items():
        row = [seneraded]

        for senerade in allSerenadesKeys:
            left = senerades.index(senerade) + 1
            right = allSerenades[senerade].index(seneraded) + 1
            index = str(left) + "," + str(right)

            row.append(index)

        inputTable.add_row(row)
    
    print(inputTable)


def stableMariageAlgorithm(swap):

    if not swap:
        # students, schools, studentsCapacities, schoolsCapacities
        allSerenades, allseneraded, serenadesCapacities, seneradedCapacities = readInput()
    else:
        # schools, students, schoolsCapacities, studentsCapacities
        allseneraded, allSerenades, seneradedCapacities, serenadesCapacities = readInput()

    # Affichage des entrées et de la première ligne
    showInput(allSerenades, allseneraded, serenadesCapacities, seneradedCapacities)
    stableMatchingtable = PrettyTable(allseneraded.keys())

    # Nombre d'itération de l'algorithme
    rounds = 0

    # Resultat final de l'algorithme
    stableMatch = {}

    # Tous les serenades sont isoles au debut
    serenadesNotMarried = allSerenades.keys()

    # Tant qu'il y a des serenades tout seul
    while (serenadesNotMarried):
        # Placer tous les serenades vers leur seneraded préféré
        serenading(allSerenades, serenadesNotMarried, serenadesCapacities, stableMatch)

        # Les serenades ont été placés
        serenadesNotMarried = []
        
        # Affichage de l'étape en cours
        row = getStableMatchingRow(allseneraded, stableMatch)    
        stableMatchingtable.add_row(row)

        # On parcours chaque seneraded pour traiter les serenades attribués
        for seneraded, serenadesToChoose in stableMatch.items():
            # Si il y a plusieurs serenades pour une seneraded
            if len(serenadesToChoose) > 1:
                # On conserve les n serenades favoris
                stableChoices = getStableChoices(serenadesToChoose, allseneraded[seneraded], seneradedCapacities[seneraded])

                # On doit redistribuer les serenades qui n'ont pas été choisi
                for serenades in serenadesToChoose:
                    if serenades not in stableChoices:
                        stableMatch[seneraded].remove(serenades)
                        serenadesNotMarried.append(serenades)
        rounds += 1

    
    print("\nResult (" + str(rounds) + " rounds):")
    print(stableMatchingtable)



def main():
    swap = False
    if len(sys.argv) > 1:
        swap = sys.argv[1] == "1"

    stableMariageAlgorithm(swap)
    

main()