# -*- coding: utf-8 -*-

import numpy as np
import yaml


# Lecture des données 
def getInput():
    Eleves = {
        "Pierre": 
            ["n7", "mine", "inp", "insa"], 
        "Clement": 
            ["inp", "insa", "n7", "mine"],
        "Philippe": 
            ["n7", "mine", "inp", "insa"],
        "Cedric": 
            ["n7", "insa", "mine", "inp"],
    }

    Ecoles = {
        "n7": 
            ["Pierre", "Clement", "Philippe", "Cedric"],
        "inp": 
            ["Cedric", "Clement", "Philippe", "Pierre"],
        "insa": 
            ["Cedric", "Pierre", "Philippe", "Clement"],
        "mine": 
            ["Philippe", "Clement", "Pierre", "Cedric"]
    }

    # Mise a jour progressivement durant l algorithme
    EcolesCourante = {
        "n7": 
            [],
        "inp": 
            [],
        "insa": 
            [],
        "mine": 
            []
    }

    return Eleves, Ecoles, EcolesCourante

# Getting input data from data.yaml
def readInput():
    with open("data.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)

            # Parsage des eleves
            Eleves = {}
            for eleve, donneeEleve in data["eleves"].items():
                Eleves[eleve] = donneeEleve["ecoles"].split()

            # Parsage des ecoles
            Ecoles = {}
            EcolesCourante = {}
            for ecole, donneeEcole in data["ecoles"].items():
                Ecoles[ecole] = donneeEcole["eleves"].split()
                EcolesCourante[ecole] = []
            
            return Eleves, Ecoles, EcolesCourante
        except yaml.YAMLError as exc:
            print(exc)


# Place les eleves isoles dans leurs ecoles favorites
def placerElevesIsoles(Eleves, ElevesIsoles, EcolesCourante):
    for eleve in ElevesIsoles:
            if Eleves[eleve]:
                # Choix de sont ecoles favorites qui ne l'a pas refuse
                c = Eleves[eleve][0]
                Eleves[eleve].pop(0)

                EcolesCourante[c].append(eleve)


# Choix de l'eleve favorie parmis une liste d'eleve a choisir
def eleveFavorie(elevesAChoisir, listePreference):
    for eleve in listePreference:
        if eleve in elevesAChoisir:
            return eleve


def stableMariage():
    Eleves, Ecoles, EcolesCourante = readInput()

    # Tous les eleves sont isoles au debut
    ElevesIsoles = Eleves.keys()

    # Tant qu'il y a des eleves sans ecole
    while (ElevesIsoles):
        # Placer tous les eleves sans ecole
        placerElevesIsoles(Eleves, ElevesIsoles, EcolesCourante)

        # Reset des eleves isoles
        ElevesIsoles = []
        
        # On parcours les ecoles (ecoles) et leurs etudiants (elevesAChoisir)
        for ecole, elevesAChoisir in EcolesCourante.items():
            # Conflit. Trop d'eleve pour une ecole, lesquels prends on ?
            if len(elevesAChoisir) > 1:
                # On conserve l'eleve favorie
                choixEleve = eleveFavorie(elevesAChoisir, Ecoles[ecole])
                    
                # On supprime les autres qui redeviennent isoles
                for eleveIsole in elevesAChoisir:
                    if eleveIsole != choixEleve:
                        EcolesCourante[ecole].remove(eleveIsole)
                        ElevesIsoles.append(eleveIsole)
        


    return EcolesCourante


print stableMariage()


# Matching ecole a capacsite egale

# Matchning capacite multiple