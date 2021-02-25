import getpass
import os
from app.kasumi import cli as kasumi
from app.keys_generator import cli as keysgen
from app.hashes import cli as hashes
from app.blockchain import cli as blockchain


def cls():
    """ Efface le contenu du terminal """
    os.system('cls' if os.name == 'nt' else 'clear')


def check_all_cmds():
    """ Effectue toutes les commandes du menu """
    kasumi.all()
    keysgen.all()
    hashes.all()
    blockchain.all()


def switch_command(cmd):
    available_cmds = {
        1: kasumi.encrypt,
        2: kasumi.decrypt,
        3: keysgen.generate_keys,
        4: hashes.generate,
        5: hashes.check,
        6: blockchain.create_proof_of_work,
        7: blockchain.check_transaction,
        8: blockchain.increment,
        9: blockchain.check_integrity,
        10: check_all_cmds,
        11: blockchain.print_blockchain,
        12: blockchain.users_wallets,
    }

    cmd_nb = 0
    try:
        cmd_nb = int(cmd)
    except ValueError:
        print('La commande entrée doit être un nombre')

    if cmd_nb in available_cmds:
        func_to_run = available_cmds.get(cmd_nb)
        func_to_run()
        input("\nAppuyez sur Entrée pour continuer...\n")
    else:
        print('La commande n\'est pas disponible')


def run():
    while True:
        print(f'Bonjour ô maître {getpass.getuser()} ! Que souhaitez vous faire aujourd’hui ? (q pour quitter)')
        print('->1<- Chiffrer un message.')
        print('->2<- Déchiffrer un message.')
        print('->3<- Générer des couples de clés publiques / privées.')
        print('->4<- Générer un hash / une empreinte.')
        print('->5<- Vérifier un hash / une empreinte.')
        print('->6<- Effectuer une preuve de travail.')
        print('->7<- Vérifier une transaction (une signature).')
        print('->8<- Débuter / incrémenter la Block-chain.')
        print('->9<- Vérifier l’intégrité de la block-chain.')
        print('->10<- I WANT IT ALL !! I WANT IT NOW !!')

        cmd = input()
        if cmd == 'q':
            print(f'Au revoir, ô maître {getpass.getuser()} !')
            break

        switch_command(cmd)
