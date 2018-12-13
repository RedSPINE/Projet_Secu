
import pandas as pd
import numpy as np
import json
from utils import *

class Distance(object):

    def __init__(self):
        self.f_source = open("./data/ground_truth.csv", "r")
        self.f_anonym = open("./data/example_files/version17bis_rep8_del.csv", "r")
        self.limit = 10

    def init_dict(self):
        lines = self.f_anonym.readlines()
        d_init= {}
        for line in lines :
            columns=line.split(',')
            if columns[0] == "id_user":
                continue
            d_init[columns[0]] = []
        self.f_anonym.close()
        self.f_anonym = open("./data/example_files/version17bis_rep8_del.csv", "r")
        return d_init

    def dist(self, n1, n2):
        #print( "-------------" + n1 + "---------" + n2 )
        #print(1-min(float(n1), float(n2))/max(float(n1),float(n2)))
        return 1-min(float(n1), float(n2))/max(float(n1),float(n2))

    def is_list_full(self, list):
        if len(list) == self.limit:
            return True
        else:
            return False

    def list_replace_last(self, list, tuple):
        """
        Remplace le dernier élément de la liste si celui ci est supérieur au nouveau
        """
        if list[self.limit-1][0] > tuple[0]:
            list[self.limit-1]= tuple

    def distance_price(self):
        """
        Pour chaque prix dans ground_truth, on compare ce prix avec chaque prix
        dans la table anonymisé. On sauvegarde les 10 distances
        (nb de distances enregistrées ajustable) les plus faibles pour chaque
        prix dans ground_truth accompagné du pseudo anonymisé associé.
        d_price = { 'id_anonym' : [(distance , 'id1'), (distance , 'id6' )...] , 'id_anonym2' : (distance , 'id45') ...}
        """
        d_price = dict(self.init_dict()) # Initialisation
        lines = self.f_anonym.readlines() # Ouverture du fichier anonym
        for line in lines : #parcours de ce fichier
            if "id_item" in line or "DEL" in line:
                continue
            columns = line.split(',')
            #print(columns[3])
            with open("./data/produits/"+columns[3]+".csv", "r") as f_id_item:  # Ouverture du fichier correspondant l'id_item
                item_lines = f_id_item.readlines()
            list=d_price.get(columns[0])
            for item_line in item_lines : # Parcours du fichier item
                #print("________________________________________________________________________")
                columns_truth = item_line.split(',')
                distance=self.dist(columns[4], columns_truth[4]) # Calculs de la distance entre les deux prix
                if self.is_list_full(list): # On vérifie que la liste correspondant à l'id user n'est pas full
                    list.sort() # On tri la liste pour pas tout parcourir en comparant
                    self.list_replace_last(list, (distance, columns_truth[0]))
                else:
                    list.append((distance, columns_truth[0])) # si la liste est pas vide on ajoue la valeur sans réfléchir
            list.sort()
            f_id_item.close()
        self.f_anonym.close()
        self.f_anonym = open("./data/example_files/version17bis_rep8_del.csv", "r")
        return d_price

    def distance_qty(self):
        """
        Pour chaque quantité dans ground_truth, on compare cette qty avec chaque qty
        dans la table anonymisé. On sauvegarde les 10 distances
        (nb de distances enregistrées ajustable) les plus faibles pour chaque
        qty dans ground_truth accompagné du pseudo anonymisé associé.
        d_price = { 'id1' : ('id_anonym', distance) , 'id2' : ('id_anonym2, distance') ...}
        """
        pass
    def distance_date(self):
        pass

def main():
    """
    main
    """
    d = Distance()
    #print(d.distance_price())
    with open("dump.json", "w") as jsdump:
        json.dump(d.distance_price() , jsdump, indent=4)
if __name__ == "__main__":
    main()
