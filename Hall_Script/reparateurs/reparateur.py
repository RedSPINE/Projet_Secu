def main() :
    f_source = open("anonym_test.csv", "r")
    f_dest = open("anonym_test_Bien.csv", "w")
    l1 = True

    for line in f_source :
        if l1 == True :
            l1 = False
            f_dest.write(line)
        else :
            if line[6] == "*" :
                f_dest.write("DEL,1111/11/11,11:11,11111,11.11,11\n")
                #f_dest.write("DEL,,,,,\n")
            else:
                curseur = 0
                while line[curseur] != "," :
                    f_dest.write(line[curseur])
                    curseur += 1
                f_dest.write(line[curseur])
                curseur += 1
                while line[curseur] != "," :
                    f_dest.write(line[curseur])
                    curseur += 1
                f_dest.write(line[curseur])
                curseur += 1
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
                f_dest.write(str((b_sup + b_inf) / 2) + ",")

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




if __name__ == "__main__":
    main()