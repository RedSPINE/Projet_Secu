def calculateur() :
    f_source = open("csv/ground_truth.csv", "r")
    l1 = True
    tab = [[] for i in range(4073)]
    for line in f_source :
        if l1 == True :
            l1 = False
        else :
            curseur = 0
            while line[curseur] != "," :
                curseur += 1
            curseur += 1
            while line[curseur] != "," :
                curseur += 1
            curseur += 1
            while line[curseur] != "," :
                curseur += 1
            curseur += 1
            while line[curseur] != "," :
                curseur += 1
            curseur += 1
            prix = 0
            while line[curseur] != "." :
                prix = prix * 10 + int(line[curseur])
                curseur += 1
            curseur += 1
            dec = 0.1
            while line[curseur] != "," :
                prix = prix + int(line[curseur])*dec
                curseur += 1
                dec /= 10
            for i in range (4073) :
                if prix < (i+1)*2 :
                    tab[i].append(prix)
                    break
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
    med_tab = [[] for i in range(4073)]
    for i in range(len(tab)) :
        med_tab[i] = mediane(tab[i])
    return med_tab


if __name__ == "__main__":
    main()
