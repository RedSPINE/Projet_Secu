def main() :
    f_source = open("csv/ground_truth.csv", "r")
    f_dest = open("csv/ground_truth_ordonne.csv", "w")
    l1 = True
    id = 1
    for line in f_source :
        curseur = 0
        name = []
        if l1 == True :
            f_dest.write("id,")
            while line[curseur] != "\n":
                f_dest.write(line[curseur])
                curseur+=1
            f_dest.write("\n")
            l1 = False
        else :
            f_dest.write(str(id))
            f_dest.write(",")

            while line[curseur] != "\n":
                f_dest.write(line[curseur])
                curseur+=1
            f_dest.write("\n")
            id+=1
            


if __name__ == "__main__":
    main()