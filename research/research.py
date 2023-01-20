import numpy as np
import pandas as pd

def read_time(file_path):
    time = []
    with open(file_path, "r") as file :
        lines = file.readlines()
        for line in lines:
            foyer = []
            writing = False
            num = ""
            for c in line:
                if c  == '[':
                    machine = []
                    writing = True
                elif c == ']':
                    if len(num) > 0:
                        machine.append(int(num))
                    num = ""
                    foyer.append(machine)
                    writing = False
                elif c == ' ':
                    continue
                
                elif c == ',' and writing:
                    if len(num) > 0:
                        machine.append(int(num))
                    num = ""
                elif writing:
                    num = num + c
            time.append(foyer)
    # print(time)
    return time

file_path_data = "research/data.csv"
file_path_time = "research/time.txt"

def get_index_by_id(id):
    dataframe = pd.read_csv(file_path_data, header=None)
    index = None
    for k, row in dataframe.iterrows():
        if id == row[0]:
            index = k
            break
    time = read_time(file_path_time)
    labels = ["LV","LL","SL","TV","FG_1","CE_1","CG","FO","PL","FG_2","CE_2"]
    d={}
    for k, label in enumerate(labels):
        d[label]=time[index][k]

    return d



