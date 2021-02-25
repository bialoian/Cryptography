# GS15 - "Block-chain" simplifiée

Université de Technologie de Troyes - Semestre A20  

### Introduction
Dans le cadre de l'UE *GS15 - Cryptologie et signature électronique*, nous avons développé une application contenant nos propres implémentations d'algorithme de chiffrement, de génération de couple de clés publique/privée, d'algorithmes de hash, de signature et de blockchain.  

### KASUMI
L'implémentation de l'algorithme de chiffrement symétrique Kasumi réalisée dans ce projet suit à la lettre les [spécifications de la 3GPP](https://www.etsi.org/deliver/etsi_ts/135200_135299/135202/07.00.00_60/ts_135202v070000p.pdf) à l'exception de deux modifications.  
- La première modification concerne la fonction fi. La fonction fi originale de la norme est remplacée par une fonction utilisant 2 S-Boxes.
Ces S-Boxes sont générées à partir de la clé de chiffrement en utilisant l'algorithme de key schedule de RC4.
- La seconde modification concerne la fonction fl qui effectue des inverses dans un corps de Galois.  
Par manque de temps et difficulté de réaliser une version optimisée, nous n'avons pas développé notre propre implémentation de l'inverse dans un corps de Galois. Nous avons utilisé le package [pyfinite](https://github.com/emin63/pyfinite) en utilisant des polynômes irréductibles codés en dur.
L'algorithme Kasumi peut être utilisé avec les modes de chiffrement ECB, CBC, PCBC, CFB, OFB, CTR et GCM. L'implémentation du Galois Counter Mode permet de vérifier l'intégrité du message une fois déchiffré.

### Couple de clé publique/privée
L'application permet la génération de clés publiques/privées ElGamal et RSA.
La différence entre ces deux types de clés réside dans l'utilisation d'un safe prime et de son générateur pour ElGamal et de deux nombres premiers pour RSA.
Le test de primalité Miller-Rabin est utilisé pour vérifier si un nombre est premier. Le test est effectué avec 40 nombres aléatoires, donnant un taux de faux positif de 4^(-40).
Pour trouver un safe prime, le générateur de nombre premier vérifie que *(prime - 1) / 2* est premier également.
L'application contient également une démonstration de l'échange de clés Diffie-Hellman entre deux couples de clé publique/privé ElGamal.
Pour trouver des nombres premiers, l'application utilise une implémentation de XORshift128.

### Fonctions de hachage
L'application contient l'implémentation de deux fonctions de hachage :  
- La première est SHA-256 en suivant le standard [FIPS 180-4](https://csrc.nist.gov/csrc/media/publications/fips/180/2/archive/2002-08-01/documents/fips180-2.pdf).
- La seconde est une fonction qui prend pour modèle le mécanisme de fonction éponge de Keccak en utilisant SHA-256 pour la fonction f. Le message à hacher est décomposé en blocs de taille inférieure à celle de l'état de la fonction éponge. Pour décomposer le message en blocs de taille fixe (256 bits), un padding similaire à celui de SHA-256 est effectué. Les blocs du message à hacher sont ensuite xorés à l'état avant chaque exécution de la fonction f jusqu'à ce que la totalité du message soit absorbé. La phase d'essorage consite à récupérer une partie du hash final avant chaque exécution de la fonction f. Ces parties de hash sont concaténées en un hash final de 512 bits.

### Génération et vérification de signature
A partir des couples de clés ElGamal et RSA, l'application est capable de produire des signatures ElGamal et RSA de texte.
Il est également possible de vérifier la validité d'une signature à partir du message, de la signature et de la clé publique du signataire pour les deux méthodes de signature.
Par manque de temps, l'implémentation d'un système de certificats n'a pas été implémenté.


### Blockchain
La blockchain réalisée permet de réaliser des transactions de cryptomonnaie entre utilisateurs. Un utilisateur de la blockchain est représenté par un wallet. Ce wallet contient le nom de l'utilisateur et ses clés publique et privée. Le montant de cryptomonnaie en possession est déterminé en repérant toutes les transactions et tous les blocs minés de l'utilisateur sur la blockchain.
La blockchain donne une récompense de minage de bloc à l'utilisateur à l'origine de la création d'un bloc. L'utilisateur gagne donc le montant arbitraire de 10 pour chaque bloc miné. Un bloc contient un minimum de une transaction à l'exception du bloc genesis. Pour récupérer cette récompense, l'utilisateur doit fournir une preuve de travail sur le bloc. Cette preuve consiste à trouver un salt tel que la concaténation du bloc avec le salt donne un hash finissant par n zéros. La fonction de hash utilisée est l'implémentation avec fonction éponge réalisée précédemment.
Toute transaction faite sur la blockchain comporte un utilisateur débité, un utilisateur crédité et un montant. La transaction est signée à l'aide de la clé privée RSA de l'utilisateur débité.
La blockchain intègre des mécanismes permettant d'éviter que des utilisateurs aient des montants de cryptomonnaie négatifs.
Les wallets des utilisateurs sont générés automatiquement s'ils ont un couple de clé publique/privée à leur nom.


### Structure du projet
Le projet suit la structure suivante :  

- `app` : Répertoire qui contient le code de l'application
- `data` : Répertoire qui contient les données utilisées et générées par l'application.

La racine du répertoire des sources contient le point d'entrée de l'application et tous les sous packages de l'application : `kasumi`, `keys_generator`, `hashes`, `blockchain` et `utils`.
Tous ces sous packages, excepté `utils`, contiennent un fichier cli.py permettant d'utiliser les fonctionnalités du package via la console.

___

## Usage

Requiert Python >=3.6

Pour lancer l'application sans l'installer :  
`python run.py`

Attention nécessite d'avoir installé la dépendance pyfinite au préalable:  
`pip install pyfinite`

### Installation
  
Pour installer l'application :  
`python setup.py install --record files_install.txt`

Pour lancer l'application, il suffit d'entrer la commande :  
`gs15_cli`

Pour désinstaller l'application, il faut conserver le fichier `files_install.txt` et executer :  
`sudo rm $(cat files_install.txt)`

### Développement
**Setup de PyCharm**  
Mettre le script path de la configuration de Python à `GS15_KASUMI\app` pour le projet.