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


# Toutes les écoles vont se proposer à leur n élèves préférés
def serenading(serenades, serenadesNotMarried, serenadesCapacities, stableMatch):

    stableChoices = []

    for serenade in serenadesNotMarried:
        # Eleve(s) favori qui ne l'a pas refuse
        for i in range(serenadesCapacities[serenade]):
            # Traiter le cas où capacite > nombre d'élève restant
            if (i < len(serenades[serenade])):
                stableChoices.append(serenades[serenade][0])
                serenades[serenade].pop(0)

        for stableChoice in stableChoices:
            if stableChoice not in stableMatch:
                stableMatch[stableChoice] = []
            stableMatch[stableChoice].append(serenade)

        # Remettre la liste des choix stable à 0 pour la prochaine école
        stableChoices.clear()


# Choix de(s) élève(s) favori parmis une liste d'eleve a choisir
def getStableChoices(serenadesToChoose, ranking, serenadedCapacity):

    stableChoices = []

    for serenade in ranking:
        if serenade in serenadesToChoose:
            stableChoices.append(serenade)
            if len(stableChoices) >= serenadedCapacity:
                return stableChoices

    return stableChoices


def stableMariageAlgorithm(swap):

    if not swap:
        # students, schools, studentsCapacities, schoolsCapacities
        serenades, serenaded, serenadesCapacities, serenadedCapacities = readInput()
    else:
        # schools, students, schoolsCapacities, studentsCapacities
        serenaded, serenades, serenadedCapacities, serenadesCapacities = readInput()

    # Nombre d'itération de l'algorithme
    rounds = 0

    # Resultat final de l'algorithme
    stableMatch = {}

    # Tous les eleves sont isoles au debut
    serenadesNotMarried = serenades.keys()

    # Tant qu'il y a des eleves sans ecole
    while (serenadesNotMarried):
        # Placer tous les eleves dans leur ecole préférée
        serenading(serenades, serenadesNotMarried, serenadesCapacities, stableMatch)

        # Les élèves ont été placés
        serenadesNotMarried = []
        
        # On parcours chaque école pour traiter les élèves attribués
        for serenadedKey, serenadesToChoose in stableMatch.items():
            # Si il y a plusieurs élèves pour une école
            if len(serenadesToChoose) > 1:
                # On conserve les n élèves favoris
                stableChoices = getStableChoices(serenadesToChoose, serenaded[serenadedKey], serenadedCapacities[serenadedKey])
                    
                # On doit redistribuer les élèves qui n'ont pas été choisi
                for serenade in serenadesToChoose:
                    if serenade not in stableChoices:
                        stableMatch[serenadedKey].remove(serenade)
                        serenadesNotMarried.append(serenade)
        rounds += 1
        

    print(stableMatch)
    print(rounds)


def main():
    swap = False
    if len(sys.argv) > 1:
        swap = sys.argv[1] == "1"

    stableMariageAlgorithm(swap)
    

main()