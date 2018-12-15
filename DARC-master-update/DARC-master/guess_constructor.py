from distance import *
from collections import OrderedDict

class Guess(object):

    def __init__(self):
        self.f_anonym="./data/example_files/version17bis_rep8_del.csv"

        self.guess=self._guess_initialisation()

    def _guess_initialisation(self):
        """Generate a virgin F^ file with DEL on each column for each id

        :return: the dictionary of id:pseudos
        """
        self.f_source = open("./data/ground_truth.csv", "r")
        lines = self.f_source.readlines()
        guess = OrderedDict()
        for line in lines :
            columns=line.split(',')
            if columns[0] == "id_user":
                continue
            guess[columns[0]] = ['DEL' for i in range(12)]
        self.f_source.close()
        return guess

    def _month_spliter(self):
        """
        Sépare le fichier anonymiser en 12 tables, une par mois
        """
        month_files=[]
        for month in range(12):
            month_files.append(open("./data/anonym_by_month/annoym"+str(month+1)+".csv" , "w"))
        with open(self.f_anonym, "r") as month_table:
            lines= month_table.readlines()
            for line in lines : #parcours de ce fichier
                if "id_user" in line:
                    continue
                columns = line.split(',')
                m = columns[1].split('/')
                month_files[int(m[1]) - 1].write(line)
        for month in range(12):
            month_files[month].close()

    def _select_best_guess(self, month):
        """
        Remplis la colonne du dict guess correspondant au mois passé au paramètre
        """
        distance_guess = Distance("./data/anonym_by_month/annoym"+str(month+1)+".csv")
        with open("jan_guess.json", "w") as jsdump:
            json.dump(distance_guess.json_dict_object() , jsdump, indent=4)
        month_dict = distance_guess.distance_qty()
        for key , element in month_dict.items():
            list=element[0:1]
            best_guess= Element(1.0, "INIT")
            for object in list:
                if object.moyenne < best_guess.moyenne:
                    best_guess = object
            if best_guess.moyenne < 0.8:
                self.guess[best_guess.id][month] = key

    def create_json(self):
        with open("guess.json", "w") as jsdump:
            json.dump(self.guess , jsdump, indent=4)

    def stat_guess(self):
        stat_list=[]
        for month in range(12):
            nb_guess=0
            nb_total=0
            for key, value in self.guess.items():
                if self.guess[key][month] == key:
                    nb_guess += 1
                nb_total += 1
            stat_list.append((nb_guess/nb_total)*100)
        return stat_list

    def write_csv(self):
        pass

def main():
    guess = Guess()
    guess._guess_initialisation()
    #guess._month_spliter()
    guess._select_best_guess(0)
    guess.create_json()
    stat = guess.stat_guess()
    print(stat[0])
if __name__ == "__main__":
    main()
