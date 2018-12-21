from distance import *
from collections import OrderedDict
from utils import *
import pandas as pd
import numpy as np


class Guess(object):

    def __init__(self, guess = None, f_anonym = "./data/example_files/version182.csv"):
        self.f_anonym=f_anonym
        # self._ground_truth = pd.read_csv('./data/ground_truth.csv', sep=',', engine='c', na_filter=False, low_memory=False)
        # self._anon_trans = pd.read_csv('./data/example_files/version17bis_rep8_del.csv', sep=',', engine='c', na_filter=False, low_memory=False)
        # self._gt_t_col = T_COL
        self.guess=guess
        if guess == None:
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
            guess[int(columns[0])] = ['DEL' for i in range(12)]
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
            for line in lines[1:] : #parcours de ce fichier
                if "DEL" in line:
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
        month_dict = distance_guess.distance_param()
        for key , element in month_dict.items():
            list=element[0:3]
            best_guess= Element(1.0, "INIT")
            for object in list:
                if object.moyenne < best_guess.moyenne:
                    best_guess = object
                self.guess[int(best_guess.id)][month] = str(key)

    def _select_best_guess_battikh(self, month):
        """
        Remplis la colonne du dict guess correspondant au mois passé au paramètre
        """
        distance_guess = Distance("./data/anonym_by_month/annoym"+str(month+1)+".csv")
        month_dict = distance_guess.distance_battikh()
        distance_guess.json_dict_object_battikh()
        for key , element in month_dict.items():
            try:
                element[0]
            except IndexError:
                continue
            self.guess[int(element[0].id)][month] = str(key)


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

    def scoring(self):
        dataframe = pd.DataFrame(data = self.guess).transpose()
        dataframe= dataframe.reset_index()
        dataframe = dataframe.rename(columns={'index':'id_user'})
        return dataframe
        # print(dataframe)
        # dataframe_original=generate_f_orig(self._ground_truth, self._anon_trans, self._gt_t_col)
        # compare_f_files(dataframe_original, dataframe)

    def make_guess(self, split=1):
        split = 1
        print(split)
        if split == 1:
            self._month_spliter()
            print("bij")
        for month in range(12):
            self._select_best_guess(month)
        self._write_csv()
        # self.create_json()
        # stat=self.stat_guess()
        # print("January :" + str(stat[0]) + "February :" + str(stat[1]) +  "March :" + str(stat[2]) +  "April :" + str(stat[3]) +
        #   "May :" + str(stat[4]) +  "June :" + str(stat[5]) +  "July :" + str(stat[6]) +  "August :" + str(stat[7])   +
        #    "September :" + str(stat[8]) +  "October :" + str(stat[9]) +  "November :" + str(stat[10]) +  "December :" +str(stat[11]))

    def make_guess_battikh(self, split=1):
        if split == 1:
            self._month_spliter()
        for month in range(12):
            self._select_best_guess_battikh(month)
        self._write_csv()


    def _write_csv(self):
        with open("F_reid_benard_v2.csv", "w") as file:
            file.write("id_user,0,1,2,3,4,5,6,7,8,9,10,11")
            for key, value in self.guess.items():
                line_csv="\n"+str(key)+","+",".join(value)
                file.write(line_csv)

def main():
    guess = Guess()
    # guess.make_guess()
    #guess._month_spliter()
    guess._select_best_guess(0)
    guess.create_json()
    guess.scoring()
    # stat = guess.stat_guess()
    # print(stat[0])
if __name__ == "__main__":
    main()
