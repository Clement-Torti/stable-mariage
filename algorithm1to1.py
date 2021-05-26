import numpy as np

# Stable marriage algorithm
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

ElevesIsoles = []

# lancer l'algorithme
isFinish = False

while (not isFinish):
    ElevesIsoles = []

    # Les eleves choisisent leur ecole preferee
    for eleve, choix in Eleves.items():
        if choix:
            c = choix[0]
            choix.pop(0)

            EcolesCourante[c].append(eleve)
    
    # Detection de conflit
    for ecole, elevesAChoisir in EcolesCourante.items():
        if len(elevesAChoisir) > 1:
            # Choix du preferer
            for eleve in Ecoles[ecole]:
                if eleve in elevesAChoisir:
                    elevesAChoisir.remove(eleve)
                    break
                
            # Rajout des eleves isoles
            for eleveIsole in elevesAChoisir:
                ElevesIsoles.append(eleveIsole)
    
    # Critere d'arret Tous les eleves ont ete place
    if not ElevesIsoles:
        isFinish = True

    # Les eleves isoles choisisent leur nouvelle preference
    for eleve in ElevesIsoles:
        if Eleves[eleve]:
            c = Eleves[eleve][0]
            Eleves[eleve].pop(0)

            EcolesCourante[c].append(eleve)
    

    


# afficher le resultat
print EcolesCourante

# Matching 1 a 1

# Matching ecole a capacsite egale

# Matchning capacite multiple