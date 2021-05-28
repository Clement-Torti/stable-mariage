# -*- coding: utf-8 -*-

import numpy as np
import yaml
import random
import sys


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
                #random.shuffle(Eleves[eleve])
                

            # Parsage des ecoles
            Ecoles = {}
            EcolesCourante = {}
            CapaciteEcoles = {}
            for ecole, donneeEcole in data["ecoles"].items():
                Ecoles[ecole] = donneeEcole["eleves"].split()
                CapaciteEcoles[ecole] = donneeEcole["capacite"]
                #random.shuffle(Ecoles[ecole])
            
            return Eleves, Ecoles, EcolesCourante, CapaciteEcoles
        except yaml.YAMLError as exc:
            print(exc)


# Place les eleves isoles dans leurs ecoles favorites
def placerElevesIsoles(Eleves, ElevesIsoles, EcolesCourante):
    for eleve in ElevesIsoles:
            if Eleves[eleve]:
                # Choix de sont ecoles favorites qui ne l'a pas refuse
                c = Eleves[eleve][0]
                Eleves[eleve].pop(0)

                if not EcolesCourante.has_key(c):
                    EcolesCourante[c] = []

                EcolesCourante[c].append(eleve)


# Choix de l'eleve favorie parmis une liste d'eleve a choisir
def eleveFavorie(elevesAChoisir, listePreference, capacite):
    choixEleves = []

    for eleve in listePreference:
        if eleve in elevesAChoisir:
            choixEleves.append(eleve)
            if len(choixEleves) >= capacite:
                return choixEleves

    return choixEleves


def stableMariageEleves():
    Eleves, Ecoles, EcolesCourante, CapaciteEcoles = readInput()


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
            # Conflit. Trop d'eleve pour une ecole
            if len(elevesAChoisir) > 1:
                # On conserve l'eleve favorie
                choixEleves = eleveFavorie(elevesAChoisir, Ecoles[ecole], CapaciteEcoles[ecole])
                    
                # On supprime les autres qui redeviennent isoles
                for eleveIsole in elevesAChoisir:
                    if not (eleveIsole in choixEleves):
                        EcolesCourante[ecole].remove(eleveIsole)
                        ElevesIsoles.append(eleveIsole)
        

    return EcolesCourante


def contacterElevesFavories(Ecoles, EcolesIsoles, ElevesCourants, CapaciteEcoles):
    for ecole in EcolesIsoles:
        capacite = CapaciteEcoles[ecole]


        minCap = min(capacite, len(Ecoles[ecole]))

        for i in range(0, minCap):
            c = Ecoles[ecole][0]
            Ecoles[ecole].pop(0)

            if not ElevesCourants.has_key(c):
                ElevesCourants[c] = []
            
            ElevesCourants[c].append(ecole)
    
            
def ecoleFavorite(ecolesAChoisir, listePreference):
    for ecole in ecolesAChoisir:
        if ecole in listePreference:
            return ecole


def stableMariageEcoles():
    termine = False

    # Lire les donnees
    Eleves, Ecoles, ElevesCourants, CapaciteEcoles = readInput()

    # Tous les eleves sont isoles au debut
    EcolesIsoles = Ecoles.keys()

    # Critere d'arret: Une ecole n'a plus d'eleve a contacter
    while not termine:
        # Une ecole va contacter ses "capacite" eleves favoris
        contacterElevesFavories(Ecoles, EcolesIsoles, ElevesCourants, CapaciteEcoles)

        EcolesIsoles = []

        # Les eleves choisissent leur ecole favorite
        for eleve, ecolesAChoisir in ElevesCourants.items():
            c = ecoleFavorite(ecolesAChoisir, Eleves[eleve])

            # Virer les autres des ecolesAChoisir
            if len(ecolesAChoisir) > 1:
                for ecole in ecolesAChoisir:
                    if ecole != c:
                        ElevesCourants[eleve].remove(ecole)
                        # Mettre l'ecole dans ecole isole
                        EcolesIsoles.append(ecole)

        # Calcul du critere d'arret
        termine = True
        for ecole in EcolesIsoles:
            if ecole:
                termine = False

    # Afficher resultat
    return ElevesCourants



def main():
    swap = False
    if len(sys.argv) > 0:
        swap = sys.argv[1] == "1"

    if swap:
        print stableMariageEcoles()
    else:
        print stableMariageEleves()
    

main()