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
            
            for student, ranking in data["eleves"].items():
                students[student] = ranking["ecoles"].split()
                #random.shuffle(students[student])
                

            # Parsage des ecoles
            schools = {}
            schoolsCapacities = {}
            for school, ranking in data["ecoles"].items():
                schools[school] = ranking["eleves"].split()
                schoolsCapacities[school] = ranking["capacite"]
                #random.shuffle(students[student])
            
            return students, schools, schoolsCapacities
        except yaml.YAMLError as exc:
            print(exc)


# Place les eleves isoles dans leurs ecoles favorites
def serenadeSchools(students, studentsNotMarried, stableMatch):
    for student in studentsNotMarried:
        # Ecole favorite qui ne l'a pas refuse
        stableChoice = students[student][0]
        students[student].pop(0)

        if stableChoice not in stableMatch:
            stableMatch[stableChoice] = []

        stableMatch[stableChoice].append(student)


# Toutes les écoles vont se proposer à leur n élèves préférés
def serenadeStudents(schools, schoolsNotMarried, schoolsCapacties, stableMatch):

    stableChoices = []

    for school in schoolsNotMarried:
        # Eleve(s) favori qui ne l'a pas refuse
        for i in range(schoolsCapacties[school]):
            # Traiter le cas où capacite > nombre d'élève restant
            if (i < len(schools[school])):
                stableChoices.append(schools[school][0])
                schools[school].pop(0)

        for stableChoice in stableChoices:
            if stableChoice not in stableMatch:
                stableMatch[stableChoice] = []
                stableMatch[stableChoice].append(school)


# Choix de(s) élève(s) favori parmis une liste d'eleve a choisir
def getFavoriteStudents(studentsToChoose, ranking, capacity):

    stableChoices = []

    for student in ranking:
        if student in studentsToChoose:
            stableChoices.append(student)
            if len(stableChoices) >= capacity:
                return stableChoices

    return stableChoices


# Choisit l'école favorite de l'élève
def getFavoriteSchool(schoolsToChoose, ranking):

    for school in ranking:
        if school in schoolsToChoose:
            return school


def stableMariageAlgorithm(swap):

    students, schools, schoolsCapacities = readInput()

    # Nombre d'itération de l'algorithme
    rounds = 0

    # Resultat final de l'algorithme
    stableMatch = {}

    # Tous les eleves sont isoles au debut
    if not swap:
        studentsNotMarried = students.keys()
    else:
        schoolsNotMarried = schools.keys()


    if not swap:
        # Tant qu'il y a des eleves sans ecole
        while (studentsNotMarried):
            # Placer tous les eleves dans leur ecole préférée
            serenadeSchools(students, studentsNotMarried, stableMatch)

            # Les élèves ont été placés
            studentsNotMarried = []
            
            # On parcours chaque école pour traiter les élèves attribués
            for school, studentsToChoose in stableMatch.items():
                # Si il y a plusieurs élèves pour une école
                if len(studentsToChoose) > 1:
                    # On conserve les n élèves favoris
                    stableChoices = getFavoriteStudents(studentsToChoose, schools[school], schoolsCapacities[school])
                        
                    # On doit redistribuer les élèves qui n'ont pas été choisi
                    for student in studentsToChoose:
                        if student not in stableChoices:
                            stableMatch[school].remove(student)
                            studentsNotMarried.append(student)
            rounds += 1
    else:
        # Tant qu'il y a des ecoles non choisis
        while (schoolsNotMarried):
            # Toutes les écoles vont se proposer à leur n élèves préférés
            serenadeStudents(schools, schoolsNotMarried, schoolsCapacities, stableMatch)

            # Les écoles ont été placés
            schoolsNotMarried = []
            
            # On parcours chaque eleve pour traiter leur choix d'école
            for student, schoolsToChoose in stableMatch.items():
                # Si il y a plusieurs ecoles pour un élève
                if len(schoolsToChoose) > 1:
                    # On conserve l'école favorite
                    stableChoice = getFavoriteSchool(schoolsToChoose, students[student])
                        
                    # On doit redistribuer les écoles qui n'ont pas été choisi
                    for school in schoolsToChoose:
                        if school != stableChoice:
                            stableMatch[student].remove(school)
                            schoolsNotMarried.append(school)
            rounds += 1
        

    print(stableMatch)
    print(rounds)


def main():
    swap = False
    if len(sys.argv) > 1:
        swap = sys.argv[1] == "1"

    stableMariageAlgorithm(swap)
    

main()