import sys
import mediateur
import dateur
from random import randrange

o_ordonate = ["oui","non"]
o_id_user = ["hash", "clair"]
o_date = ["mediane", "fixe", "clair"]
o_hours = ["fixe", "clair"]
o_id_item = ["hash", "clair"]
o_price = ["mediane", "moyenne"]
o_qty = ["moyenne"]
ordonate  = ""
id_user = ""
date = ""
hours = ""
id_item = ""
price = ""
qty = ""
f_source = ""
f_dest = ""

def configurateur() :
    conf = open("reparateur.conf", "r")
    nb_line = 0
    for line in conf :
        curseur = 0
        while line[curseur] != ":" :
            curseur += 1
        curseur += 1
        option = []
        while line[curseur] != ";" :
            option.append(line[curseur])
            curseur += 1
        option = "".join(option)
        if nb_line == 0 :
            if option in o_ordonate :
                global ordonate 
                ordonate = option
            else :
                print("Erreur de configuration : option ordonate.")
                return -1
        elif nb_line == 1 :
            if option in o_id_user :
                global id_user
                id_user = option
            else :
                print("Erreur de configuration : option id_user.")
                return -1
        elif nb_line == 2 :
            if option in o_date :
                global date
                date = option
            else :
                print("Erreur de configuration : option date.")
                return -1
        elif nb_line == 3 :
            if option in o_hours :
                global hours
                hours = option
            else :
                print("Erreur de configuration : option hours.")
                return -1
        elif nb_line == 4 :
            if option in o_id_item :
                global id_item
                id_item = option
            else :
                print("Erreur de configuration : option id_item.")
                return -1
        elif nb_line == 5 :
            if option in o_price :
                global price
                price = option
            else :
                print("Erreur de configuration : option price.")
                return -1
        elif nb_line == 6 :
            if option in o_qty :
                global qty
                qty = option
            else :
                print("Erreur de configuration : option qty.")
                return -1
        nb_line += 1
    conf.close()
    return 1

def first_line(l1, line) :
    if l1 == True :
        l1 = False
        curseur = 0
        while line[curseur] != "," :
            curseur += 1
        curseur += 1
        while line[curseur] != "\n" :
            f_dest.write(line[curseur])
            curseur += 1
        f_dest.write("\n")
    return 1

def main() :
    if len(sys.argv) == 1 :
        print("Erreur : Pas de fichier précisé.")
        return -1
    elif len(sys.argv) > 2 :
        print("Erreur : Trop d'argument. Seul le nom du fichier est nécessaire.")
        return -1
    else :
        fichier = sys.argv[1]
        if configurateur() == -1 :
            return -1
        else :
            global f_source
            f_source = open(fichier+".csv", "r")
            global f_dest
            f_dest = open(fichier+"_rep.csv", "w")

            l1 = True
            sel = [str(hash(str(randrange(314159265359)))) for i in range(13)]
            med_tab = mediateur.main()
            med_tab_0 = dateur.main()
            
            for line in f_source :
                first_line(l1, line)

                ##################################################


            f_source.close()
            f_dest.close()
            

            
        
        


if __name__ == "__main__":
    main()