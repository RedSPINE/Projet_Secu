import mediateur
import dateur

def main() :
    f_source = open("version18.csv", "r")
    f_source2 = open("ground_truth.csv", "r")
    f_dest = open("version181.csv", "w")
    l1 = True

    med_tab = mediateur.main()
    med_tab_0 = dateur.main()

    for line in f_source :
        if l1 == True :
            l1 = False
            f_dest.write(line)
        else :
            if '*' in line :
                f_dest.write("DEL,1111/11/11,11:11,11111,11.11,11\n")
                #f_dest.write("DEL,,,,,\n")
            else:
                curseur = 0
                name = []
                while line[curseur] != "," :
                    name.append(line[curseur])
                    curseur += 1
                name = str(''.join(name))
                f_dest.write(str(hash(str(hash(name)))))
                f_dest.write(line[curseur])
                curseur += 1
                while line[curseur] != "/" :
                    f_dest.write(line[curseur])
                    curseur += 1
                curseur += 1
                f_dest.write("/")
                mois = 0
                while line[curseur] != "/" :
                    mois = mois * 10 + int(line[curseur])
                    f_dest.write(line[curseur])
                    curseur += 1
                curseur += 1
                f_dest.write("/")
                while line[curseur] != "," :
                    curseur += 1
                curseur += 1
                if med_tab_0[mois-1] < 10:
                    f_dest.write("0")
                f_dest.write(str(int(med_tab_0[mois-1])) + ",")
                f_dest.write("13:37,")
                curseur += 6
                while line[curseur] != "," :
                    f_dest.write(line[curseur])
                    curseur += 1
                f_dest.write(line[curseur])
                curseur += 3

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
                curseur += 7
                if b_inf > len(med_tab) :
                    f_dest.write(str(med_tab[len(med_tab)-1]) + ",")
                else :
                    f_dest.write(str(med_tab[b_inf//2]) + ",")


                #f_dest.write(str((b_sup + b_inf) / 2) + ",")

                if line[curseur] == "-" :
                    negatif = -1
                    curseur += 1
                else :
                    negatif = 1

                b_inf = 0
                b_sup = 0
                while line[curseur] != "," :
                    b_inf = b_inf * 10 + int(line[curseur])
                    curseur += 1
                curseur += 2
                b_inf *= negatif

                if line[curseur] == "-" :
                    negatif = -1
                    curseur += 1
                else :
                    negatif = 1

                while line[curseur] != "[" :
                    b_sup = b_sup * 10 + int(line[curseur])
                    curseur += 1
                f_dest.write(str(int((b_sup + b_inf) / 2)) + "\n")


    f_source.close()
    f_dest.close()
    prix_compare(
        open("ground_truth.csv", "r"),
        open("version181.csv", "r"),
        open("version182.csv", "w")
    )


def prix_compare(f_source, f_source2, f_dest):
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

if __name__ == "__main__":
    main()
