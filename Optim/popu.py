import numpy as np
import pandas as pd
from foyer import Foyer


class Popu:

    def __init__(self, dataframe):
        self.elements = self.create_elem(dataframe)
        self.g_conso = self.get_g_conso()

        self.best = None

        self.fit = None
        self.compute_fit()
        # self.compute_fit2()
        self.best_fit = self.fit

        self.best_vois = None

    def create_elem(self, dataframe):
        elems = []

        for index, row in dataframe.iterrows():
            area = int(row[0][1:].split("-")[0])
            machine_used = row[1:].to_numpy()
            elems.append(Foyer(area, machine_used))
        return elems

    def get_g_conso(self):
        g_conso = [0]*48
        for k in range(len(self.elements)):
            tab = self.elements[k].conso
            for i, elem in enumerate(tab):
                g_conso[i] += elem
        
        return g_conso

    def compute_fit(self):
        self.g_conso = self.get_g_conso()

        tot = sum(self.g_conso)/ len(self.g_conso)
        d = 0
        for e in self.g_conso:
            d+= abs(e- tot)
        self.fit = d

    def compute_fit2(self):
        self.g_conso = self.get_g_conso()
        self.fit = max(self.g_conso)


    def update_best_pos(self):
        if self.fit < self.best_fit:
            self.best_fit = self.fit
            for f in self.elements:
                f.update_best_pos()
            

    def get_data(self):
        res = []
        for k in range(len(self.elements)):
            res.append(self.elements[k].pos)
        return np.array(res)

    def update(self, g_best, loop):
        for k in range(len(self.elements)):
            if k%1000 == 0:
                print(f"{loop} -> Element {k}")
            self.elements[k].update(g_best[k])
        