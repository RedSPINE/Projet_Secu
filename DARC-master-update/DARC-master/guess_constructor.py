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

    def _dict_gen(self, dist_object, method):
        if method == "pqty":
            month_dict = dist_object.distance_by_pqty_match()
        elif method == "qty":
            month_dict = dist_object.distance_by_qty_match()
        else:
            month_dict = dist_object.distance_param()
        return month_dict

    def _select_best_guess_by_dist(self, month, method, nb_element):
        """
        Remplis la colonne du dict guess correspondant au mois passé au paramètre
        """
        distance_guess = Distance("./data/anonym_by_month/annoym"+str(month+1)+".csv")
        month_dict = self._dict_gen(distance_guess, method)
        for key , element in month_dict.items():
            list=element[0:nb_element]
            best_guess= Element(1.0, "INIT")
            for object in list:
                if object.moyenne < best_guess.moyenne:
                    best_guess = object
                self.guess[int(best_guess.id)] = str(key)

    def _select_first_guess(self, month, method):
        """
        Remplis la colonne du dict guess correspondant au mois passé au paramètre
        """
        distance_guess = Distance("./data/anonym_by_month/annoym"+str(month+1)+".csv")
        month_dict = self._dict_gen(distance_guess, method)
        for key , element in month_dict.items():
            try:
                element[0]
            except IndexError:
                continue
            self.guess[int(element[0].id)][month] = str(key)

    def create_json(self):
        with open("guess.json", "w") as jsdump:
            json.dump(self.guess , jsdump, indent=4)

    def make_guess(self, month, method, nb_element=1):
        if nb_element == 1:
            self._select_first_guess(month, method)
        else:
            self._select_best_guess_by_dist(month, method, nb_element)

    def _write_csv(self):
        with open("F_reid_hecht_v2.csv", "w") as file:
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
    # stat = guess.stat_guess()
    # print(stat[0])
if __name__ == "__main__":
    main()
