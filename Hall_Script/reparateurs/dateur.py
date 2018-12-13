def calculateur() :
    f_source = open("ground_truth.csv", "r")
    l1 = True
    tab = [[] for i in range(12)]
    for line in f_source :
        if l1 == True :
            l1 = False
        else :
            curseur = 0
            while line[curseur] != "," :
                curseur += 1
            curseur += 1
            while line[curseur] != "/" :
                curseur += 1
            curseur += 1
            mois = 0
            while line[curseur] != "/" :
                mois = mois * 10 + int(line[curseur])
                curseur += 1
            curseur += 1
            jour = 0
            while line[curseur] != "," :
                jour = jour * 10 + int(line[curseur])
                curseur += 1
            tab[mois-1].append(jour)
    f_source.close()
    return tab

def mediane(l):
    l = sorted(l)
    l_len = len(l)
    if l_len < 1:
        return None
    if l_len % 2 == 0 :
        return round(( l[(l_len-1)//2] + l[(l_len+1)//2] ) / 2.0, 2)
    else:
        return round(l[(l_len-1)//2], 2)

def main() :
    tab = calculateur()
    med_tab = [[] for i in range(12)]
    for i in range(len(tab)) :
        med_tab[i] = mediane(tab[i])
    return med_tab


if __name__ == "__main__":
    main()
