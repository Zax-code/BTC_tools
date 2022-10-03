# BTC_tools
TD2 de Blockchain programming de Hugo Schneegans et Zakaria Abouliatim

Pour utiliser cet outil : 
- Cloner le projet github puis ouvrez une invite de commande dans le dossier cloné
- Utiliser la commande "pip install -r requirements.txt" afin d'installer les libraries nécessaires ( 2 libraires à installer )
- Lancer le programme en lançant le fichier main.py avec la commande "python main.py"

Ce projet a avancé sans accro jusqu'au moment de s'attaquer à la dérivation de clé enfant avec le protocole BIP32, en effet, nous avons :
 - Géneré une seed aléatoire
 - Retranscrit cette seed en suite mnémonique ( en implémentant son opposé pour permettre l'import de mnémonique )
 - Extrait la master private key et la chaincode associées à une seed entrée
 - Extrait la master public key à partir de la private key précédemment extraite

Et tout cela manuellement en utilisant uniquement des librairies mathématiques pour les différentes fonctions de hashage nécessaires aux différentes protocole BTC
Cependant la dérivation de clé en clés enfants nécessite beaucoup plus de manipulation mathématique et après plusieurs heures de recherches nous avons finalement compris la théorie derrière,
malgré cela, l'implémentation de cette théorie nécessite des créations de classes notamment pour les calculs de points de la normale aux courbes elliptiques qui demande beaucoup de temps et de connaissances en programmation python.
Nous avons cherché une alternative comme une libraire qui feraient ces calculs sans avoir à passer par la création d'une classe Point en vain.
Nous avons finalement décidé de s'appuyer sur la libraire BIP32 en python permettant tout simplement de déterminer des clés enfants à partir d'une seed donnée et d'un chemin de dérivation.

Nous avons néanmoins fait une tentative de fonction permettant d'obtenir une clé enfant à partir d'un chemin de dérivation qui ne fonctionne malheureusement pas (il manque la partie ajoutant un extrait de la clé parent qui est justement la partie nécessitant la théorie mathématique qui s'appuie sur les courbes elliptique)

En tout cas, toutes les actions du menu sont fonctionnelles, on peut effectivement importer une seed à partir d'une suite mnémonique puis utiliser cette seed pour obtenir les master keys (public et private) et également obtenir les clés enfants de tout type de dérivation (le tout en hexadecimal)
Attention ! Il faut d'abord importer ou générer une seed avant de pouvoir faire toute autre action du menu

Ce qui nous manquerait pour avoir une véritable boite à outil Bitcoin serait la transcription de ces clés en extended keys avec un encodage en base58 pour être dans le format qu'utilisent tous les acteurs BTC d'aujourd'hui pour manipuler les clés
Hugo Schneegans et Zakaria Abouliatim
