# -*- coding: utf-8 -*-

import numpy as np
import yaml
import random
import sys


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


# Tous les serenades vont se proposer à leur n serenaded préférés
def serenading(allSerenades, serenadesNotMarried, serenadesCapacities, stableMatch):

    stableChoices = []

    for serenades in serenadesNotMarried:
        # Serenaded favori(s) qui ne l'a pas refuse
        for i in range(serenadesCapacities[serenades]):
            # Traiter le cas où capacite > nombre de serenaded restant
            if (i < len(allSerenades[serenades])):
                stableChoices.append(allSerenades[serenades][0])
                allSerenades[serenades].pop(0)

        for stableChoice in stableChoices:
            if stableChoice not in stableMatch:
                stableMatch[stableChoice] = []
            stableMatch[stableChoice].append(serenades)

        # Remettre la liste des choix stable à 0 pour le prochain serenades
        stableChoices.clear()


# Choix de(s) serenade(s) favori parmis la liste de préférence du serenaded
def getStableChoices(serenadesToChoose, ranking, serenadedCapacity):

    stableChoices = []

    for serenades in ranking:
        if serenades in serenadesToChoose:
            stableChoices.append(serenades)
            # Un serenaded ne peut pas choisir plus de serenades que sa capacitié
            if len(stableChoices) >= serenadedCapacity:
                return stableChoices

    return stableChoices


def stableMariageAlgorithm(swap):

    if not swap:
        # students, schools, studentsCapacities, schoolsCapacities
        allSerenades, allSerenaded, serenadesCapacities, serenadedCapacities = readInput()
    else:
        # schools, students, schoolsCapacities, studentsCapacities
        allSerenaded, allSerenades, serenadedCapacities, serenadesCapacities = readInput()

    # Nombre d'itération de l'algorithme
    rounds = 0

    # Resultat final de l'algorithme
    stableMatch = {}

    # Tous les serenades sont isoles au debut
    serenadesNotMarried = allSerenades.keys()

    # Tant qu'il y a des serenades tout seul
    while (serenadesNotMarried):
        # Placer tous les serenades vers leur serenaded préféré
        serenading(allSerenades, serenadesNotMarried, serenadesCapacities, stableMatch)

        # Les serenades ont été placés
        serenadesNotMarried = []
        
        # On parcours chaque serenaded pour traiter les serenades attribués
        for serenaded, serenadesToChoose in stableMatch.items():
            # Si il y a plusieurs serenades pour une serenaded
            if len(serenadesToChoose) > 1:
                # On conserve les n serenades favoris
                stableChoices = getStableChoices(serenadesToChoose, allSerenaded[serenaded], serenadedCapacities[serenaded])
                    
                # On doit redistribuer les serenades qui n'ont pas été choisi
                for serenades in serenadesToChoose:
                    if serenades not in stableChoices:
                        stableMatch[serenaded].remove(serenades)
                        serenadesNotMarried.append(serenades)
        rounds += 1
        

    print(stableMatch)
    print(rounds)


def main():
    swap = False
    if len(sys.argv) > 1:
        swap = sys.argv[1] == "1"

    stableMariageAlgorithm(swap)
    

main()