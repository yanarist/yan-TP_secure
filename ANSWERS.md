PRISE EN MAIN

Q1
Cette typologie s'appelle client-serveur avec deux clients qui se connectent au même serveur. Deux clients interagissent avec un serveur commun.

Q2
Les logs enregistrent les actions effectuées par le serveur et les clients ainsi que les messages échangés. On peut suivre le déroulement de la communication entre les différents acteurs. Cela peut être important pour le débogage et la surveillance du système.

Q3
Cela est un problème notamment en matière de sécurité puisque cela signifie que ces messages peuvent être lus et modifiés par n'importe qui (les messages ne soient pas chiffrés). Cela contrevient au principe de sécurité de Kerckhoffs où la sécurité d'un système ne doit pas dépendre du secret de l'algorithme, mais plutôt de la clé.

Q4
Pour éviter cela, une solution simple consisterait à utiliser un algorithme de chiffrement symétrique tel que l'AES pour crypter le message. Ensuite, la clé de chiffrement symétrique pourrait être chiffrée avec la clé publique du destinataire, et les deux éléments chiffrés seraient ensuite transmis. Le destinataire pourrait alors utiliser sa clé privée pour déchiffrer la clé de chiffrement symétrique et alors décrypter le message.


CHIFFREMENT

Q1
La fonction "urandom" n'est pas le meilleur choix pour la cryptographie. Elle génère des nombres aléatoires en Python. Cependant, elle n'est pas considérée comme suffisamment sécurisée car les valeurs qu'elle donne peuvent être prévisibles dans certaines conditions.

Q2
L'utilisation de primitives cryptographiques peut-être dangereux puisqu'il faut comprendre en profondeur leur fonctionnement afin de détecter et de corriger les vulnérabilités potentielles. Si il y a un petit manque de compréhension, il existe un risque que l'implémentation ne soit pas totalement sécurisée.

Q3
Malgré le chiffrement, un serveur malveillant peut nuire encore puisqu'il peut toujours perturber le fonctionnement du système en envoyant des données incorrectes.

Q4
Il manque la propriété d'authentification, qui pourrait être mise en œuvre en utilisant un HMAC (Code d'authentification basé sur un hachage).


AUTHENTIFICATED SYMETRIC ENCRYPTION

Q1
Fernet est moins risqué en termes d'implémentation puisqu'il gère automatiquement les problèmes de remplissage (padding). De plus, la clé secrète est générée automatiquement, ce qui réduit les risques liés au choix d'une clé faible ou prédictible.

Q2
Un serveur malveillant peut néanmoins attaquer avec des faux messages avec une attaque appelée "replay attack"; Elle consiste à renvoyer des messages précédemment interceptés pour tromper le destinataire.

Q3
Pour se protéger contre les attaques de "replay", nous pouvons ajouter un identifiant unique à chaque message. Cela permet de garantir que le message reçu est réellement nouveau et n'a pas été intercepté et renvoyé ultérieurement.


TTL

Q1
À première vue, il peut sembler qu'il n'y ait pas de différence significative par rapport au chapitre précédent.

Q2
Si on soustrait au tempps lors de l'émisson, il y a une différence importante. Elle réside dans le fait que le destinataire ne pourra pas déchiffrer le message si le timestamp associé au message dépasse sa durée de vie (Time-to-Live). Le message ne sera plus considéré comme valide, même s'il est correctement chiffré.

Q3
L'ajout d'une durée de vie (TTL) au message peut en effet contribuer à se prémunir contre les attaques de "replay" si le délai est suffisamment court pour empêcher la réutilisation de messages précédemment émis.

Q4
En prratique, cette approche peut présenter des limites puisqu'il faut maintenir une synchronisation minutieuse des horloges entre les systèmes et la gestion de l'historique des numéros de séquence ou des horodatages pour chaque message.

Regard critique
La librairie Fernet utilisée pour chiffrer les messages présente quelques vulnérabilités. Par exemple, elle ne peut pas gérer efficacement les messages de grande taille, et elle utilise une fonction pseudo-aléatoire pour générer les vecteurs d'initialisation (IV), ce qui peut les rendre prédictibles. De plus, bien que les messages soient chiffrés, les noms des destinataires restent en clair, ce qui peut permettre de déduire qui communique avec qui. Ces vulnérabilités pourraient être exploitées pour intercepter ou tronquer des messages.
