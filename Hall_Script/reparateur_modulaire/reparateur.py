import sys
import os
import mediateur
import dateur
from random import randrange

o_ordonate = ["oui","non"]
o_id_user = ["hash", "clair"]
o_date = ["mediane", "fixe", "clair"]
o_hours = ["fixe", "clair"]
o_id_item = ["hash", "clair"]
o_price = ["mediane", "moyenne", "clair"]
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
sel_client = [str(hash(str(randrange(314159265359)))) for i in range(13)]

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
    curseur = 0
    global ordonate
    if ordonate == "oui" :
        while line[curseur] != "," :
            curseur += 1
        curseur += 1
    while line[curseur] != "\n" :
        f_dest.write(line[curseur])
        curseur += 1
    f_dest.write("\n")
    return False


def delete(line) :
    curs = 0
    while line[curs] != "\n" :
        curs += 1
    if line[curs - 1] == "*" :
        f_dest.write("DEL,1111/11/11,11:11,11111,11.11,11\n")
        return True
    else :
        return False


def order(line, curseur) :
    global ordonate
    if ordonate == "oui" :
        while line[curseur] != "," :
            curseur += 1
        curseur += 1
    return curseur


def client(line, curseur) :
    global id_user
    global f_dest
    user = []
    while line[curseur] != "," :
        user.append(line[curseur])
        curseur += 1
    user = "".join(user)
    if id_user == "hash" :
        c = curseur + 1
        annee = []
        while line[c] != "/" :
            annee.append(line[c])
            c += 1
        if "".join(annee) == "2010" : 
            mois = 13
        else :
            c += 1
            mois = 0
            while line[c] != "/" :
                mois = mois * 10 + int(line[c])
                c += 1
        f_dest.write(str(hash(str(hash(user[::-1] + sel_client[mois-1]))[::-1])))
    elif id_user == "clair" :
        f_dest.write(user)
    f_dest.write(",")
    curseur += 1
    return curseur


def dates(line, curseur, med_tab) :
    global date
    global f_dest

    # Années 
    annee = []
    while line[curseur] != "/" :
        f_dest.write(line[curseur])
        annee.append(line[curseur])
        curseur += 1
    f_dest.write(line[curseur])
    curseur += 1

    # Mois
    if "".join(annee) == "2010" :
        mois = 13
        f_dest.write("12/")
        curseur += 3
    else :
        mois = 0
        while line[curseur] != "/" :
            mois = mois * 10 + int(line[curseur])
            f_dest.write(line[curseur])
            curseur += 1
        f_dest.write(line[curseur])
        curseur += 1

    # Jours
    if date == "mediane" :
        jour = str(int(med_tab[mois-1]))
        if int(jour) < 10 :
            jour = "0" + str(jour)
        f_dest.write(jour)
        curseur += 2
    elif date == "fixe" :
        f_dest.write("15")
        curseur += 2
    elif date == "clair" :
        while line[curseur] != "," :
            f_dest.write(line[curseur])
            curseur += 1
    f_dest.write(",")
    curseur += 1
    return curseur


def heure(line, curseur) :
    global hours
    global f_dest
    if hours == "fixe" :
        f_dest.write("13:37")
        curseur += 5
    elif hours == "clair" :
        while line[curseur] != "," :
            f_dest.write(line[curseur])
            curseur += 1
    f_dest.write(",")
    curseur += 1
    return curseur


def objet(line, curseur) :
    global id_item
    global f_dest
    item = []
    while line[curseur] != "," :
        item.append(line[curseur])
        curseur += 1
    item = "".join(item)
    if id_item == "hash" :
        sel = str(hash(str(randrange(314159265359))))
        f_dest.write(str(hash(str(hash(item[::-1] + sel))[::-1])))
    elif id_item == "clair" :
        f_dest.write(item)
    f_dest.write(",")
    curseur += 1
    return curseur


def prix(line, curseur, med_tab) :
    global price
    global f_dest
    if price == "clair" :
        while line[curseur] != "," :
            f_dest.write(line[curseur])
            curseur += 1
        f_dest.write(",")
        curseur += 1
    else :
        curseur += 2
        b_inf = 0
        b_sup = 0
        while line[curseur] != "." :
            b_inf = b_inf * 10 + int(line[curseur])
            curseur += 1
        curseur += 1
        while line[curseur] != "," :
            curseur += 1
        curseur += 2

        while line[curseur] != "." :
            b_sup = b_sup * 10 + int(line[curseur])
            curseur += 1

        if price == "mediane" :
            f_dest.write(str(med_tab[b_inf//2]))
        elif price == "moyenne" :
            f_dest.write(str((b_sup + b_inf)/2))

        
        f_dest.write(",")
        curseur += 5
    return curseur


def quantite(line, curseur) :
    global qty
    global f_dest
    curseur += 2

    b_inf = 0
    b_sup = 0
    neg = 1
    if line[curseur] == "-" :
        neg = -1
        curseur += 1
    while line[curseur] != "," :
        b_inf = b_inf * 10 + int(line[curseur])
        curseur += 1
    b_inf *= neg
    curseur += 2
    neg = 1
    if line[curseur] == "-" :
        neg = -1
        curseur += 1
    while line[curseur] != "[" :
        b_sup = b_sup * 10 + int(line[curseur])
        curseur += 1
    
    if qty == "moyenne" :
        f_dest.write(str(int(((b_sup + b_inf)/2))))
    
    while line[curseur] != "\n" :
        curseur += 1

    return curseur


def extreme(f_source, f_source2, f_dest):
    lines = f_source.readlines()
    lines2= f_source2.readlines()
    for line,line2 in zip(lines, lines2):
        if "price" in line:
            f_dest.write(line2)
            continue
        columns=line.split(',')
        columns2= line2.split(',')
        if 1-min(float(columns[4]), float(columns2[4]) )/max(float(columns2[4]), float(columns2[4])) > 0.85:
            f_dest.write("DEL,1111/11/11,11:11,11111,11.11,11\n")
        else:
            f_dest.write(line2)


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
            f_source = open("csv/"+fichier+".csv", "r")
            global f_dest
            f_dest = open("csv/"+fichier+"_tmp.csv", "w")

            l1 = True
            date_med_tab = dateur.main()
            prix_med_tab = mediateur.main()

            for line in f_source :
                curseur = 0
                if l1 :
                    l1 = first_line(l1, line)
                    continue
                if not delete(line) :
                    curseur = order(line, curseur)
                    curseur = client(line, curseur)
                    curseur = dates(line, curseur, date_med_tab)
                    curseur = heure(line, curseur)
                    curseur = objet(line, curseur)
                    curseur = prix(line, curseur, prix_med_tab)
                    curseur = quantite(line, curseur)
                    f_dest.write("\n")
            
            f_source.close()
            f_dest.close()    

            extreme(open("csv/ground_truth.csv", "r"), open("csv/"+fichier+"_tmp.csv", "r"), open("csv/"+fichier+"_rep.csv", "w"))

            os.remove("csv/"+fichier+"_tmp.csv")

            


if __name__ == "__main__":
    main()