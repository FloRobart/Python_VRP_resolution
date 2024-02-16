# Rapport sur la modélisation du problème et la concpetion d'une interface graphique

<div class="page"></div>

## Table des matières

- [Rapport sur la modélisation du problème et la concpetion d'une interface graphique](#rapport-sur-la-modélisation-du-problème-et-la-concpetion-dune-interface-graphique)
  - [Table des matières](#table-des-matières)
  - [Modélisation mathématique du problème](#modélisation-mathématique-du-problème)
  - [Modélisation CPlex du problème](#modélisation-cplex-du-problème)
  - [Conception de l'interface graphique](#conception-de-linterface-graphique)
    - [Librairie utilisée](#librairie-utilisée)
  - [Implémentation de l'API de CPlex](#implémentation-de-lapi-de-cplex)
    - [Définition des Contraintes et des Variables](#définition-des-contraintes-et-des-variables)
    - [Importation des Données](#importation-des-données)
    - [Résolution du Problème avec CPLEX](#résolution-du-problème-avec-cplex)
    - [Génération des Solutions et du Graphe](#génération-des-solutions-et-du-graphe)
    - [Problème rencontré](#problème-rencontré)

<div class="page"></div>

## Introduction

Le projet en question se penche sur une problématique cruciale dans le domaine de la logistique et de la distribution : l'optimisation des tournées d'une flotte de véhicules chargés de livrer divers clients à partir d'un dépôt central. Cette tâche complexe est caractérisée par la présence de plusieurs contraintes, telles que la capacité limitée de chaque véhicule, l'obligation de satisfaire la demande spécifique de chaque client, et la nécessité pour chaque véhicule de retourner au dépôt après avoir effectué sa tournée. L'objectif principal de ce projet est de développer des solutions efficaces pour minimiser la distance parcourue par l'ensemble des véhicules, optimisant ainsi le processus de livraison dans son ensemble. Il convient de noter que ce défi s'inscrit dans la lignée du problème classique du voyageur de commerce, mais avec des paramètres supplémentaires qui le rendent plus réaliste et pertinent pour des contextes logistiques spécifiques.

<div class="page"></div>

## Modélisation mathématique du problème

### Données du problème

Les données du problème, cruciales pour le projet d'optimisation des tournées d'une flotte de véhicules, sont énumérées ci-dessous, chacune étant accompagnée d'une explication :

- **C :**
  - Nombre de clients.

- **N :**
  - Ensemble des clients, où N = {1, 2, ..., C}.

- **Vertices :**
  - Ensemble de sommets (ou nœuds), où Vertices = 101 ∪ N.

- **A :**
  - Ensemble d'arêtes, où A = {(i, j) ∈ V^2 : i ≠ j}.

- **dist_ij :**
  - Distance entre les arêtes (i, j) ∈ A.

- **Q :**
  - Capacité.

- **demande_i :**
  - Demande du client i ∈ N.

- **V :**
  - Nombre de véhicules.

- **Vehicules :**
  - Ensemble de véhicules.

### Variable de décision

Les variables de décision définies dans le cadre du projet d'optimisation des tournées d'une flotte de véhicules sont fondamentales pour modéliser le problème. Voici une liste de ces variables, accompagnée d'explications :

- **xvij :**
  - Variable binaire égale à 1 si le véhicule v passe directement du nœud i au nœud j, et 0 sinon.

- **nbreVehiculeUtilise :**
  - Nombre de véhicules utilisés.


### Contraintes

Les contraintes énoncées dans le projet d'optimisation des tournées d'une flotte de véhicules sont cruciales pour définir le cadre du problème. Voici une liste des contraintes accompagnées d'explications :

1. **Un véhicule qui quitte le dépôt, retourne au dépôt à la fin de sa tournée :**
   - Chaque véhicule doit commencer et terminer sa tournée au dépôt, garantissant ainsi une gestion efficace des ressources et une meilleure planification des itinéraires.

2. **Un véhicule visite un client une et une seule fois :**
   - Chaque client doit être servi par un seul véhicule, évitant ainsi les redondances dans les livraisons et garantissant l'efficacité de la distribution.

3. **Au moins un véhicule est utilisé pour la construction des tournées :**
   - Assure qu'il y a au moins un véhicule en activité, ce qui est essentiel pour accomplir les livraisons et satisfaire la demande des clients.

4. **Un seul véhicule est utilisé pour aller de i à j :**
   - Chaque trajet entre deux clients doit être effectué par un seul véhicule, ce qui simplifie la gestion des itinéraires et la coordination des ressources.

5. **Un client est visité exactement une et une seule fois par un véhicule :**
   - Chaque client doit être inclus dans l'itinéraire d'un seul véhicule pour éviter la confusion et garantir une livraison précise et complète.

6. **Élimination des sous-tours :**
   - Empêche la formation de sous-tours, où un véhicule pourrait retourner au dépôt avant d'avoir desservi tous les clients prévus dans sa tournée. Cette contrainte garantit une planification logique et optimale des itinéraires.

7. **La capacité du véhicule ne peut être dépassée :**
   - Chaque véhicule a une capacité maximale définie, assurant ainsi que la somme des produits à livrer à chaque client dans une tournée ne dépasse pas cette capacité. Cette contrainte est essentielle pour maintenir l'efficacité opérationnelle de la flotte.

### Modèle mathématique



## Modélisation CPlex du problème



## Conception de l'interface graphique

Pour réaliser l'interface graphique de notre application, nous avons utilisé plusieurs librairies Python. Parmi ces librairies, nous avons utilisé la librairie 'sys' pour manipuler les paramètres liés à l'exécution du script, la librairie 'PyQt5.QtWidgets' pour créer des composants d'interface utilisateur (UI) et des éléments graphiques, la librairie 'PyQt5.QtGui' pour enrichir les capacités graphiques de l'application, et la librairie 'PyQt5.QtCore' pour assurer le bon fonctionnement de l'architecture de l'application PyQt5.


### Librairie utilisée

'sys'

Le module sys est une bibliothèque standard de Python qui fournit un accès à certaines fonctionnalités spécifiques du système. En particulier, l'importation de sys est couramment utilisée pour manipuler des paramètres liés à l'exécution du script, tels que les arguments de la ligne de commande. Il offre également des fonctionnalités pour interagir avec l'environnement d'exécution, comme la gestion des chemins d'accès et la sortie standard.

'PyQt5.QtWidgets'

Le module PyQt5.QtWidgets fait partie de la bibliothèque PyQt5, qui est une liaison Python pour la bibliothèque graphique Qt. Ce module fournit des composants d'interface utilisateur (UI) et des éléments graphiques essentiels pour le développement d'applications GUI. En important PyQt5.QtWidgets, vous avez accès à des classes telles que les fenêtres, les boutons, les boîtes de dialogue, etc., facilitant ainsi la création d'interfaces utilisateur interactives et conviviales.

'PyQt5.QtGui'

Le module PyQt5.QtGui offre des fonctionnalités graphiques supplémentaires pour le développement d'interfaces utilisateur. Il inclut des éléments tels que les polices, les couleurs, les images, et d'autres outils graphiques. En important ce module, vous enrichissez les capacités graphiques de votre application PyQt5, permettant la manipulation avancée des composants visuels et des éléments esthétiques.

'PyQt5.QtCore'

Le module PyQt5.QtCore est un composant fondamental de PyQt5, fournissant des fonctionnalités de base pour le développement d'applications. Il offre des classes liées à la gestion des événements, aux signaux et aux slots, ainsi qu'à la manipulation du temps et des threads. Importer PyQt5.QtCore est crucial pour assurer le bon fonctionnement de l'architecture de l'application PyQt5, en facilitant la gestion des interactions utilisateur et des tâches concurrentes.


## Implémentation de l'API de CPlex

Pour résoudre le problème d'optimisation à l'aide de CPLEX, nous avons intégré l'API CPLEX dans notre programme Python. L'utilisation de l'API a été réalisée en respectant les étapes suivantes :

### Définition des Contraintes et des Variables

Les contraintes et les variables du modèle d'optimisation ont été spécifiées en utilisant les fonctionnalités fournies par l'API DOCplex. Les contraintes et variables sont déclarées directement dans le code Python, en utilisant les méthodes et les classes fournies par l'API pour construire le modèle de manière intuitive et efficace.

```python
from docplex.mp.model import Model

# Création du modèle
model = Model('NomDuModele')

# Déclaration des variables
x = model.integer_var_dict( ... )
# Déclaration des contraintes
model.add_constraint( ... )
```

### Importation des Données

Les données nécessaires pour résoudre le problème sont importées à partir d'un fichier généré par une application externe. Ces données sont ensuite traitées à l'aide d'un programme spécifique qui convertit une matrice de coordonnées en une matrice de distances. Les données résultantes sont ensuite intégrées dans le modèle CPLEX pour être utilisées lors de la résolution du problème.

```python
# Importation des données à partir d'un fichier externe
donnees = importer_donnees('chemin/vers/fichier.csv')

# Traitement des données pour obtenir la matrice de distances
matrice_distances = convertir_en_matrice_distances(donnees)

# Utilisation des données dans le modèle
model.add_constraints( ... )
```

### Résolution du Problème avec CPLEX

Une fois que le modèle a été construit et que les données ont été importées, nous utilisons l'API CPLEX pour résoudre le problème d'optimisation. La résolution se fait en appelant la méthode solve() du modèle.

```python
# Résolution du modèle
solution = model.solve()

# Obtention des résultats
if solution:
    # Traitement et affichage des résultats
    afficher_resultats(solution)
else:
    print("Aucune solution trouvée.")
```

### Génération des Solutions et du Graphe

Les solutions obtenues après la résolution du modèle sont exploitées pour générer les résultats finaux. L'API DOCplex facilite la récupération des valeurs des variables, ce qui permet de créer le graphe de manière dynamique.

```python
# Récupération des valeurs des variables
variables_solution = solution.get_all_values()

# Génération du graphe
generer_graphe(variables_solution)
```

En suivant cette approche, nous avons pu intégrer l'API CPLEX de manière transparente dans notre programme Python, simplifiant ainsi le processus de modélisation, de résolution et de visualisation des résultats.

### Problème rencontré

- **Problème de compatibilité:** Si nous voulons lire un fichier avec l'API CPlex en Python, nous sommes limité à une fourchette d'extensions de fichier. Qui sont le MPS, le LP et le SAV. Hors, le fichier de données que nous devons lire est un fichier .dat, qui n'est pas compatible avec l'API CPlex.
