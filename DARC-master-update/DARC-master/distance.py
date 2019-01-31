
import pandas as pd
import numpy as np
import json
from utils import *
from datetime import datetime

SINGLE_MATCH_ALLOWED = 1

class Element(object):
    """
    This class defines what an element is for our guess_dict
    and has methods to update these attributes
    """

    def __init__(self, distance, id):
        self.total_distance = distance #distance total where distance is the distance between original and guess
        self.id = id #id user guess
        self.nb_element = 1 # nb_element find for this id
        self.moyenne= distance # mean distance

    def update_distance(self, distance):
        self.total_distance += distance

    def update_element(self, nb_element):
        self.nb_element += nb_element

    def update_moyenne(self):
        self.moyenne = self.total_distance/self.nb_element

    def update(self, distance, nb_element):
        self.update_distance(distance)
        self.update_element(nb_element)
        self.update_moyenne()

    def single_id_item_update(self):
        self.nb_element += 1000
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

    def __init__(self, AT):
        self.f_source = open("./data/ground_truth.csv", "r")
        self.f_anonym = AT
        self.limit = 50
        #this limit has been choosen in order to improve the reidentification time, it can be changed

    def init_dict(self):
        """
        Initialization of the guess_dict, this guess dict has for key id_users
        from the csv_file and for value a list. This list will contain element
        from the Element class
        """
        file_to_read = open(self.f_anonym, "r")
        lines = file_to_read.readlines()
        d_init= {}
        for line in lines :
            columns=line.split(',')
            if columns[0] == "id_user":
                continue
            d_init[columns[0]] = []
        file_to_read.close()
        return d_init

    def dist(self, n1, n2):
        #print( "-------------" + n1 + "---------" + n2 )
        #print(1-min(float(n1), float(n2))/max(float(n1),float(n2)))
        n1=abs(float(n1))
        n2=abs(float(n2))
        if float(n1) != 0.0 and float(n2) != 0.0 :
            return 1-min(float(n1), float(n2))/max(float(n1),float(n2))
        else :
            return 0.0

    def is_list_full(self, list):
        """
        Not really usefull
        """
        if len(list) == self.limit:
            return True
        else:
            return False

    def list_replace_last(self, list, element):
        """
        Replace the last element from the by the new if the old element has an higher
        mean than the new
        """
        if list[self.limit-1].get_moyenne() > element.total_distance:
            list[self.limit-1]= element

    def list_append(self, list, element):
        """
        If the element is already in the list we update total_distance and
        the mean and increment nb_element otherwise we just add the element in the list
        """
        for id in list:
            if id.id == element.id:
                id.update(element.total_distance, element.nb_element)
                return
        if self.is_list_full(list):
            list.sort(key=lambda x: x.get_nb_element(), reverse = True)
            self.list_replace_last(list, element)
        else:
            list.append(element) # si la liste est pas vide on ajoue la valeur sans réfléchir

    def distance_by_qty_match(self):
        """
        La spéciale rey, on regarde les qty, mais on garde que ce qui match
        """
        d_rey = dict(self.init_dict()) # Initialisation
        anonym_file = open(self.f_anonym, "r")
        lines = anonym_file.readlines() # Ouverture du fichier anonym
        for line in lines : #parcours de ce fichier
            if "id_item" in line or "DEL" in line:
                continue
            columns = line.split(',')
            #print(columns[3])
            with open("./data/produits/"+columns[3]+".csv", "r") as f_id_item:  # Ouverture du fichier correspondant l'id_item
                item_lines = f_id_item.readlines()
            list=d_rey.get(columns[0])
            for item_line in item_lines : # Parcours du fichier item
                #print("________________________________________________________________________")
                columns_truth = item_line.split(',')
                distance=self.dist(columns[5], columns_truth[5]) # Calculs de la distance entre les deux quantité
                if distance == 0.0:
                    element=Element(distance, columns_truth[0])
                    if len(item_lines) == 1 and SINGLE_MATCH_ALLOWED == 1:
                        element.single_id_item_update()
                    self.list_append(list, element)
            list.sort(key=lambda x: x.get_nb_element(), reverse = True)
            f_id_item.close()
        anonym_file.close()
        return d_rey

    def distance_dateqty(self):

        d_param = dict(self.init_dict()) # Initialisation
        anonym_file = open(self.f_anonym, "r")
        lines = anonym_file.readlines() # Ouverture du fichier anonym
        for line in lines : #parcours de ce fichier
            if "id_item" in line or "DEL" in line:
                continue
            columns = line.split(',')
            #print(columns[3])
            with open("./data/produits/"+columns[3]+".csv", "r") as f_id_item:  # Ouverture du fichier correspondant l'id_item
                item_lines = f_id_item.readlines()
            list=d_param.get(columns[0])
            for item_line in item_lines : # Parcours du fichier item
                #print("________________________________________________________________________")
                columns_truth = item_line.split(',')
                distance=self.dist(columns[5], columns_truth[5]) # Calculs de la distance entre les deux quantité
                date1 = datetime.strptime(columns[1], "%Y/%m/%d")
                date2 = datetime.strptime(columns[1], "%Y/%m/%d")
                if date1.year == date2.year:
                    distance2= self.dist(date1.timetuple().tm_yday, date1.timetuple().tm_yday)#tm_yday is the day number within the current year starting with 1 for January 1st.
                    element=Element(distance2, columns_truth[0])
                    self.list_append(list, element)

                element=Element(distance, columns_truth[0])
                self.list_append(list, element)
            list.sort(key=lambda x: x.get_nb_element(), reverse = True)
            f_id_item.close()
        anonym_file.close()
        return d_param

    def distance_date(self):

        d_param = dict(self.init_dict()) # Initialisation
        anonym_file = open(self.f_anonym, "r")
        lines = anonym_file.readlines() # Ouverture du fichier anonym
        for line in lines : #parcours de ce fichier
            if "id_item" in line or "DEL" in line:
                continue
            columns = line.split(',')
            #print(columns[3])
            with open("./data/produits/"+columns[3]+".csv", "r") as f_id_item:  # Ouverture du fichier correspondant l'id_item
                item_lines = f_id_item.readlines()
            list=d_param.get(columns[0])
            for item_line in item_lines : # Parcours du fichier item
                #print("________________________________________________________________________")
                columns_truth = item_line.split(',')
                date1 = datetime.strptime(columns[1], "%Y/%m/%d")
                date2 = datetime.strptime(columns[1], "%Y/%m/%d")
                if date1.year == date2.year:
                    distance= self.dist(date1.timetuple().tm_yday, date1.timetuple().tm_yday)#tm_yday is the day number within the current year starting with 1 for January 1st.
                    element=Element(distance, columns_truth[0])
                    self.list_append(list, element)
            list.sort(key=lambda x: x.get_nb_element(), reverse = True)
            f_id_item.close()
        anonym_file.close()
        return d_param

    def distance_by_pqty_match(self):
        """
        La spéciale battikh, on regarde et les prix et les qty, mais on garde que ce qui match
        """
        d_battikh = dict(self.init_dict()) # Initialisation
        anonym_file = open(self.f_anonym, "r")
        lines = anonym_file.readlines() # Ouverture du fichier anonym
        for line in lines : #parcours de ce fichier
            if "id_item" in line or "DEL" in line:
                continue
            columns = line.split(',')
            #print(columns[3])
            with open("./data/produits/"+columns[3]+".csv", "r") as f_id_item:  # Ouverture du fichier correspondant l'id_item
                item_lines = f_id_item.readlines()
            list=d_battikh.get(columns[0])
            for item_line in item_lines : # Parcours du fichier item
                #print("________________________________________________________________________")
                columns_truth = item_line.split(',')
                distance=self.dist(columns[5], columns_truth[5]) # Calculs de la distance entre les deux quantité
                distance2= self.dist(columns[4], columns_truth[4])
                if distance2 == 0.0:
                    element=Element(distance2, columns_truth[0])
                    if len(item_lines) == 1 and SINGLE_MATCH_ALLOWED == 1:
                        element.single_id_item_update()
                    self.list_append(list, element)
                elif distance == 0.0:
                    element=Element(distance, columns_truth[0])
                    if len(item_lines) == 1 and SINGLE_MATCH_ALLOWED == 1:
                        element.single_id_item_update()
                    self.list_append(list, element)
            list.sort(key=lambda x: x.get_nb_element(), reverse = True)
            f_id_item.close()
        anonym_file.close()
        return d_battikh


    def distance_param(self, value=5):
        """
        Pour chaque quantité dans ground_truth, on compare cette quantité avec chaque quantité
        dans la table anonymisé. On sauvegarde les 10 distances
        (nb de distances enregistrées ajustable) les plus faibles pour chaque
        quantité dans ground_truth accompagné du pseudo anonymisé associé.
        d_param = { 'id_anonym' : [(distance , 'id1'), (distance , 'id6' )...] , 'id_anonym2' : (distance , 'id45') ...}

        ----------IMPORTANT----------- Pour utiliser ce code pour les prix, passé value = 6
        """
        d_param = dict(self.init_dict()) # Initialisation
        anonym_file = open(self.f_anonym, "r")
        lines = anonym_file.readlines() # Ouverture du fichier anonym
        for line in lines[1:] : #parcours de ce fichier
            if "id_item" in line or "DEL" in line:
                continue
            columns = line.split(',')
            #print(columns[3])
            try:
                with open("./data/produits/"+columns[3]+".csv", "r") as f_id_item:  # Ouverture du fichier correspondant l'id_item
                    item_lines = f_id_item.readlines()
            except FileNotFoundError:
                print("TRICHEUR")
                continue
            list=d_param.get(columns[0])
            for item_line in item_lines : # Parcours du fichier item
                columns_truth = item_line.split(',')
                distance=self.dist(columns[5], columns_truth[5]) # Calculs de la distance entre les deux quantité
                element=Element(distance, columns_truth[0])
                if len(item_lines) == 1 and SINGLE_MATCH_ALLOWED == 1:
                    element.single_id_item_update()
                self.list_append(list, element)
            list.sort(key=lambda x: x.get_nb_element(), reverse = True)
            f_id_item.close()
        anonym_file.close()
        return d_param

    def json_dict_object(self):
        dict = self.distance_param()
        new_dict= {}
        for key , element in dict.items():
            list = []
            for object in element:
                list.append(object.serialize())
            new_dict[key] = list
        return new_dict

    def json_dict_object_battikh(self):
        dict = self.distance_battikh()
        new_dict= {}
        for key , element in dict.items():
            list = []
            for object in element:
                list.append(object.serialize())
            new_dict[key] = list
        with open("battikh.json", "w") as jsdump:
            json.dump(new_dict , jsdump, indent=4)
        return new_dict

def main():
    """
    main
    """
    d = Distance("./data/example_files/version17bis_rep8_del.csv")
    #print(d.distance_param())
    with open("dump.json", "w") as jsdump:
        json.dump(d.json_dict_object() , jsdump, indent=4)

if __name__ == "__main__":
    main()
