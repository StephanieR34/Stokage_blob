Ceci est script pour envoyer ou récupere des données 
sur un compte de stockage AzureBlob

avant de le lancer vous devez compléter le fichier .ini
en completant :

restordir : le dossier qui va ressevoir les fichiers telecharcher 
account : c'est ton compte de stockage
container: conteneur créer dans compte de stockage
key: votre clé 

Ensuite pour lancer le programme taper 
python main.py list  pour avoir la liste des fichier present sur le conteneur

python main.py upload <nomdufichier> pour envoyer un fichier 

python main.py download <nomdufichier> pour telecharger un fichier

si vous voulez changer de fichier de configuration :
pyhon main.py -cfg <nouveaufichier de config> <commande desirés>

si vous voulez changer le niveau de logging:
python main.py -lvl <niveau log> <commande désirés>