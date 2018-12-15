
import pandas as pd
import numpy as np
import json
from utils import *

class Element(object):

    def __init__(self, distance, id):
        self.total_distance = distance
        self.id = id
        self.nb_element = 1
        self.moyenne= distance

    def update_distance(self, distance):
        self.total_distance += distance

    def update_element(self):
        self.nb_element += 1

    def update_moyenne(self):
        self.moyenne = self.total_distance/self.nb_element

    def update(self, distance, nb_element):
        self.update_distance(distance)
        self.update_element()
        self.update_moyenne()

    def serialize(self):
        return {
            "total_distance" : self.total_distance,
            "id" : self.id,
            "nb_element" : self.nb_element,
            "moyenne" : self.moyenne
        }
    def get_moyenne(self):
        return self.moyenne

    def get_nb_element(self):
        return self.nb_element

class Distance(object):

    def __init__(self):
        self.f_source = open("./data/ground_truth.csv", "r")
        self.f_anonym = open("./data/example_files/version17bis_rep8_del.csv", "r")
        self.limit = 50

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
        """
        Peut être plus utile
        """
        if len(list) == self.limit:
            return True
        else:
            return False

    def list_replace_last(self, list, element):
        """
        Remplace le dernier élément de la liste si celui ci est supérieur au nouveau
        Peut être plus utile
        """
        if list[self.limit-1].get_moyenne() > element.total_distance:
            list[self.limit-1]= element

    def list_append(self, list, element ):
        for id in list:
            if id.id == element.id:
                id.update(element.total_distance, element.nb_element)
                return
        if self.is_list_full(list):
            list.sort(key=lambda x: x.get_nb_element(), reverse = True)
            self.list_replace_last(list, element)
        else:
            list.append(element) # si la liste est pas vide on ajoue la valeur sans réfléchir



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
                distance=self.dist(columns[5], columns_truth[5]) # Calculs de la distance entre les deux prix
                element=Element(distance, columns_truth[0])
                self.list_append(list, element)
            list.sort(key=lambda x: x.get_nb_element(), reverse = True)
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

    def json_dict_object(self):
        dict = self.distance_price()
        new_dict= {}
        for key , element in dict.items():
            list = []
            for object in element:
                list.append(object.serialize())
            new_dict[key] = list
        return new_dict

def main():
    """
    main
    """
    d = Distance()
    #print(d.distance_price())
    with open("dump.json", "w") as jsdump:
        json.dump(d.json_dict_object() , jsdump, indent=4)
if __name__ == "__main__":
    main()
