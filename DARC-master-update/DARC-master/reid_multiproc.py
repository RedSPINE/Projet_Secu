import guess_constructor as gc
from collections import OrderedDict
from distance import *
from utils import *
from pathos.multiprocessing import ProcessingPool as Pool
from multiprocessing import Queue
from multiprocess import Manager
GUESS_PART = list()
NB_MONTH = 13
import time
#IDEA, if there is only one item in a product table, add this element with a high score
def show_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        retour = func(*args, **kwargs)
        print(time.time() - start)
        return retour
    return wrapper

def month_spliter(f_anonym):
    """
    Split the anonymized file into 12 tables
    """
    month_files=[]
    for month in range(13):
        month_files.append(open("./data/anonym_by_month/annoym"+str(month+1)+".csv" , "w"))
    with open(f_anonym, "r") as month_table:
        lines= month_table.readlines()
        for line in lines[1:] : #parcours de ce fichier
            if "DEL" in line:
                continue
            columns = line.split(',')
            m = columns[1].split('/')
            if int(m[0]) == 2010:
                month_files[int(m[1])].write(line)
            else:
                month_files[int(m[1]) - 1].write(line)
    for month in range(13):
        month_files[month].close()

def write_csv(g_1, g_2, g_3, g_4, g_5, g_6, g_7, g_8, g_9, g_10, g_11, g_12, g_13):
    """
    Write csv built on the guess made by our threads, we combine their results
    and we write csv.
    """
    with open("F_reid_hecht_v2.csv", "w") as file: #f_dest should become a user's choice
        file.write("id_user,0,1,2,3,4,5,6,7,8,9,10,11,12")
        for (key, value), (key2, value2), (key3, value3), (key4, value4), (key5, value5), (key6, value6), (key7, value7), (key8, value8), (key9, value9), (key10, value10), (key11, value11), (key12, value12), (key13, value13) in zip(g_1.items(), g_2.items(), g_3.items(), g_4.items(), g_5.items(), g_6.items(), g_7.items(), g_8.items(), g_9.items(), g_10.items(), g_11.items(), g_12.items(), g_13.items()):
            # We iterate on our 3 dicts in the same time thanks to zip()
            line_csv="\n"+str(key)+","+value+","+value2+","+value3+","+value4+","+value5+","+value6+","+value7+","+value8+","+value9+","+value10+","+value11+","+value12+","+value13
            file.write(line_csv)

class Reid(object):
    """
    This class is the threeading class for reidentification. Threading allow us
    to reduce the time needed for running the reidentification by spliting the task
    for each month in different thread.
    The way we split is define in the main
    """

    def __init__(self, file_to_attack, method_order, nb_element):
        self._users=self._M_init()
        self._users_t_col=M_COL
        self.path = file_to_attack
        self.method_order = method_order
        self.nb_element = 3

    def _M_init(self):
        """
        Here we reuse some of the metrics code, in _M_init we have all we need
        for the F_file_init in order to have the same dict that in the original
        metrics code
        """
        T = pd.read_csv('./data/ground_truth.csv', sep=',', engine='c', na_filter=False, low_memory=False)
        T.columns = T_COL.values()
        M = T[T_COL['id_user']].value_counts()
        M = list(M.index)
        M.sort()
        M = pd.DataFrame(M, columns=M_COL.values())
        return M

    def _F_file_init(self):
        """
        This method initialize in numeric order the f_file dictionary
        """
        f_file = OrderedDict()
        for row in self._users.itertuples():
            # Fill dic[id] with DEL
            f_file[row[self._users_t_col['id_user']]] = 'DEL'
        return f_file

    def reid(self, month):
        print("BIJ")
        find_guess = gc.Guess(self._F_file_init(), self.path)
        # We create a Guess object (see guess_constructor.py)
        find_guess.make_guess(month, self.method_order, self.nb_element)
        #with lock:
        #GUESS_PART.append((month, find_guess.guess))
        print("I'LL DO IT")
        return (month, find_guess.guess)

def maker(month , queue):
    file_to_attack = './data/example_files/S_Soumission_Aymane_1.csv'
    method_order = 'param'
    nb_element = 1
    reid = __import__("reid_multiproc")
    R=reid.Reid(file_to_attack, method_order, nb_element)
    queue.put(R.reid(month))
    print("I DIT IT")
    return 0

def main():
    """
    main
    """
    file_to_attack = './data/example_files/S_hecht_submission_3.csv'
    method_order = 'param'
    nb_element = 1
    month_spliter(file_to_attack)
    manager = Manager()
    queue_list=[manager.Queue(1) for _ in range(13)]
    with Pool(6) as p:
        print("HEY")
        p.map(maker, [i for i in range(13)], queue_list)
    for queue in queue_list:
        GUESS_PART.append(queue.get())
    GUESS_PART.sort()
    for i in range(NB_MONTH):
        char = "guess_par_t"+ str(i) + ".json"
        with open(char, "w") as jsdump:
            json.dump(GUESS_PART[i][1] , jsdump, indent=4)
    write_csv(GUESS_PART[0][1], GUESS_PART[1][1] , GUESS_PART[2][1], GUESS_PART[3][1],
    GUESS_PART[4][1] , GUESS_PART[5][1], GUESS_PART[6][1], GUESS_PART[7][1] , GUESS_PART[8][1], GUESS_PART[9][1], GUESS_PART[10][1] , GUESS_PART[11][1], GUESS_PART[12][1] )

if __name__ == "__main__":
    main()
