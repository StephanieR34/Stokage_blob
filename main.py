import sys
import argparse
import configparser # permet l'utilisation des variable du fichier config
import logging
import os.path
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
# BlobServiceClient: La classe BlobServiceClient vous permet de manipuler les ressources de stockage Azure et les conteneurs blob.
# ContainerClient : La classe ContainerClient vous permet de manipuler des conteneurs de stockage Azure et leurs blobs.
# BlobClient : La classe BlobClient vous permet de manipuler des blobs de stockage Azure.


def listb(args, containerclient):
    """
    this function return one list of all of file
    on the blob storage 

    """
    logging.info("fonctions de récupération de la liste des fichiers présent sur le blob")
    blob_list=containerclient.list_blobs()
    for blob in blob_list:
        print(blob.name)


def upload(cible, blobclient):
    """
    this function upload one file from our pc
    to your blob storage

    """
    logging.info(f"Ouverture du fichier {cible} pour l'envoyer ")
    with open(cible, "rb") as f:
        logging.warning(f"envois des fichiers sur le container {blobclient}")
        blobclient.upload_blob(f)


def download(filename, dl_folder, blobclient):
    """
    this function download one file of your choice 
    from your blob storage to your pc

    """
    logging.info(f"Ouverture du fichier {filename} pour le telecharger ")
    with open(os.path.join(dl_folder,filename), "wb") as my_blob:
        logging.warning(f"recuperation des fichiers {filename} sur le container {blobclient}")
        blob_data=blobclient.download_blob()
        blob_data.readinto(my_blob)


def main(args,config):
    """
    cible un compte de stockage, puis cible un container puis
    en fonction des arguments passer en ligne de commande elle lance la fonction adapté
    
    si l'argument entrée en ligne de commande est list
    la fonction listb returne l'intituler de tout les blobs 
    contnues dans le conteneur Azure 

    si l'argument upload et spécifier en ligne de commande 
    cette fonction prend le chemin d'accés du fichier passer en ligne de commande aussi 
    et envois ce ficher sur le conteneur Azure

    si l'argument download suivit d'un noms de fichier
    est passer en ligne de commande cette fonction 
    va télecharger le fichier demander depuis le container de stockage
    Azur sur le pc client   
    """
    logging.info("lancement de la fonction main")
    blobclient=BlobServiceClient(
        f"https://{config['storage']['account']}.blob.core.windows.net",
        config["storage"]["key"],
        logging_enable=False)
    logging.debug("connection au compte de stockage effectuer")
    containerclient=blobclient.get_container_client(config["storage"]["container"])
    logging.debug("connection au container de stockage")
    if args.action=="list":
        """
        si l'argument entrée en ligne de commande est list
        la fonction listb returne l'intituler de tout les blobs 
        contnues dans le conteneur Azure 
        """
        logging.debug("l'arg list a été passé. Lancement de la fonction liste")
        return listb(args, containerclient)
    else:
        if args.action=="upload":
            blobclient=containerclient.get_blob_client(os.path.basename(args.cible))
            logging.debug("arg upload a été passé. Lancement de la fonction upload")
            return upload(args.cible, blobclient)
        elif args.action=="download":
            logging.debug("arg download a été passé. Lancement de la fonction download")
            blobclient=containerclient.get_blob_client(os.path.basename(args.remote))
            return download(args.remote, config["general"]["restoredir"], blobclient)
    

if __name__=="__main__":
    # définition des différents arguments 
    parser=argparse.ArgumentParser("Logiciel d'archivage de documents")
    parser.add_argument("-cfg",default="config.ini",help="chemin du fichier de configuration")
    parser.add_argument("-lvl",default="info",help="niveau de log")
    subparsers=parser.add_subparsers(dest="action",help="type d'operation")
    subparsers.required=True
    
    parser_s=subparsers.add_parser("upload")
    parser_s.add_argument("cible",help="fichier à envoyer")

    parser_r=subparsers.add_parser("download")
    parser_r.add_argument("remote",help="nom du fichier à télécharger")
    
    parser_r=subparsers.add_parser("list")

    args=parser.parse_args()

    
    loglevels={"debug":logging.DEBUG, "info":logging.INFO, "warning":logging.WARNING, "error":logging.ERROR, "critical":logging.CRITICAL}
    

    logging.basicConfig(level=loglevels[args.lvl.lower()])
    
    config=configparser.ConfigParser()
    config.read(args.cfg)

    sys.exit(main(args,config))