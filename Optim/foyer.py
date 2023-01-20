import numpy as np
import copy
from math import ceil

PSI = 0.3
P1 = 0.3
P2 = 0.7


class Foyer:
    hc = []
    machine_data = []
    hc_start = None
    hc_len = None    


    def set_hc(h_start, h_end):
        """
        Set the static argument hc (heures creuses)

        Arguments:
        ----------
        h_start : int
            half hour (between 0 and 47) corresponding to the start of the hc time

        h_end : int
            half hour (between 0 and 47) corresponding to the and of the hc time
        """
        if h_start < 0 or h_end <0 or h_start > 47 or h_end > 47:
            raise Exception("invalid arguments : h_start and h_end not between 0 and 47")

        i = h_start
        while i != h_end:
            Foyer.hc.append(i)
            i = (i+1) % 48 
        print(Foyer.hc)
        Foyer.hc_start = h_start
        print(Foyer.hc_start)
        Foyer.hc_len = len(Foyer.hc)


    def set_static_data(data):
        """
        Set the static argument machine_data 
        machine_data is a list in which each elemnt correspond to a start hour
        each elem is a dict {"puissance": int, 
                            "intensity": int, 
                            "usage_time": nb of half hour,
                            "seq": bool,
                            "hc": bool,
                            "nb_cycle": int}

        Arguments:
        ----------
        data : dict
            similar to machine_data, but with key (for user) instead of index
        """
        for k, value in data.items():
            # if value["seq"]:
            #     nb_call = value["usage_time"] *2* value["nb_cycle"]
            #     value["nb_cycle"] = nb_call
            #     value["usage_time"] = 0.5
            #     Foyer.machine_data.append(value)
            # else:
            Foyer.machine_data.append(value)
        # print(Foyer.machine_data)

    def __init__(self, area, machine_used):

        self.max_puiss = self._get_max_puiss(area)

        self.pos = self._init_pos(machine_used)
        self.best_pos = self.pos.copy()

        self.conso = self.get_conso()
  
        self.vit = []
        for machine in self.pos:
            self.vit.append([3]*len(machine))


    def _get_max_puiss(self, area):
        if area < 50:
            return 3000
        if area < 80:
            return 6000
        if area < 100:
            return 9000
        if area < 160:
            return 12000
        if area < 180:
            return 15000
        if area < 200:
            return 25000
        if area < 250:
            return 30000
        else :
            return 36000

    def _init_pos(self, machine_used):
        pos = []
        for index, object in enumerate(machine_used):
            
            if object:
                if Foyer.machine_data[index]["hc"]:
                    machine_planning = np.random.choice(Foyer.hc, Foyer.machine_data[index]["nb_cycle"], False)
                else:
                    machine_planning = np.random.choice(range(48), Foyer.machine_data[index]["nb_cycle"], False)
                pos.append(sorted(machine_planning))
            else:
                pos.append([])
                
        return np.array(pos)


    def get_conso(self):
        conso = np.zeros(48)
        for i, machine in enumerate(self.pos):
            if len(machine) != 0:
                for hr in machine:
                    k = 0
                    for k in range(hr, hr + ceil(Foyer.machine_data[i]["usage_time"]*2)):
                        conso[(k)%48] +=  Foyer.machine_data[i]["puissance"]
        return conso.tolist()

    def update_best_pos(self):
        for k_machine in range(len(self.pos)):
            for k_hour in range(len(self.pos[k_machine])):
                self.best_pos[k_machine][k_hour] = self.pos[k_machine][k_hour]

    def update(self, best):
        for k_machine in range(len(self.pos)):
            if len(self.pos[k_machine]) > 0:
                for k_hour in range(len(self.pos[k_machine])):
                    self.vit[k_machine][k_hour] = PSI * self.vit[k_machine][k_hour] + \
                                            P1 * (self.best_pos[k_machine][k_hour] - self.pos[k_machine][k_hour]) + \
                                            P2 * (best[k_machine][k_hour] - self.pos[k_machine][k_hour]) 

                    if abs(self.vit[k_machine][k_hour]) < 1 and np.random.uniform(0.05):
                        self.vit[k_machine][k_hour] = 1 * (self.vit[k_machine][k_hour] / abs(self.vit[k_machine][k_hour]))

                self.pos[k_machine][k_hour] = round(self.pos[k_machine][k_hour] + self.vit[k_machine][k_hour]) % 48

        # bornes
        self.validate_pos()
        # self.conso = self.get_conso()
        info = self.is_valid()
        if info:
            print(info)

    def validate_pos(self):
        # No machine using twice the same half hour
        for machine in self.pos :
            if len(machine) > 1:
                for k in range(1, len(machine)):
                    while machine[k] == machine[(k-1) % 48]:
                        machine[k] += 1

        # If in hc, stay in hc
        for index, machine in enumerate(self.pos) :
            if Foyer.machine_data[index]["hc"]:
                for k in range(len(machine)):
                    if machine[k] not in Foyer.hc:
                        self.move_to_next_hr(index, k, True)

        self.conso = self.get_conso()
        hr_pb = self.check_conso() 
        while hr_pb !=-1:
            k_machine, k_hour = self.get_machine_in_hr(hr_pb)
            self.move_to_next_hr(k_machine, k_hour, Foyer.machine_data[k_machine]["hc"])
            self.conso = self.get_conso()
            hr_pb = self.check_conso() 

    def check_conso(self):
        for k in range(48):
            conso = self.get_conso()
            if conso[k] > self.max_puiss:
                return k
        return -1
    
    def get_machine_in_hr(self, hr_pb):
        k_strat = np.random.randint(11)
        for k_machine in range(k_strat, k_strat + 11):
            for k_hour, hr in enumerate(self.pos[k_machine%11]):
                if (hr_pb - hr)%48 <= ceil(Foyer.machine_data[k_machine%11]["usage_time"]*2):
                    return k_machine%11, k_hour
        print(hr_pb)
        print(self.conso)
        print(self.get_conso())
        print(self.pos)
        raise Exception("No machine at this hour")


    def move_to_next_hr(self,k_machine, k_hour, hc):
        if hc:
            while True:
                if (self.pos[k_machine][k_hour]+1 - Foyer.hc_start)% 48 < Foyer.hc_len and \
                                ((self.pos[k_machine][k_hour]+1)%48) not in self.pos[k_machine]:

                    self.pos[k_machine][k_hour] = (self.pos[k_machine][k_hour] + 1) % 48
                    break

                self.pos[k_machine][k_hour] = (self.pos[k_machine][k_hour] + 1) % 48
        else:
            self.pos[k_machine][k_hour] = (self.pos[k_machine][k_hour] + 1) % 48

    def is_valid(self):
        self.conso = self.get_conso()
        for k, conso_hr in enumerate(self.conso):
            if conso_hr > self.max_puiss:
                print(f"overflow puissance : {k}")
                return 2

        for index, machine in enumerate(self.pos):
            if Foyer.machine_data[index]["hc"]:
                for hr in machine:
                    if not hr in Foyer.hc:
                        print(f"PB : {hr}")
                        return 1
        

        return 0