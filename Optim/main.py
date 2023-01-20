import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from foyer import Foyer
from popu import Popu

machine_data = {"LV" : {"puissance":1300 ,"intensity": 6,"usage_time": 1,"seq": False,"hc": False,"nb_cycle": 1},
                "LL" : {"puissance":2000 ,"intensity": 9,"usage_time": 1,"seq": False,"hc": False,"nb_cycle": 1},
                "SL" : {"puissance":1000 ,"intensity": 4,"usage_time": 4,"seq": False,"hc": False,"nb_cycle": 1},
                "TV" : {"puissance":100 ,"intensity": 0.5,"usage_time": 4,"seq": False,"hc": True,"nb_cycle": 1},
                "FG_1" : {"puissance":100 ,"intensity": 0.5,"usage_time": 0.2,"seq": False,"hc": True,"nb_cycle":4},
                "CE_1" : {"puissance":2200 ,"intensity": 10,"usage_time": 6,"seq": True,"hc": True,"nb_cycle": 1},
                "CG" : {"puissance":100 ,"intensity": 0.5,"usage_time": 0.2,"seq": False,"hc": True,"nb_cycle": 4},
                "FO" : {"puissance":1600 ,"intensity": 12,"usage_time": 0.75,"seq": False,"hc": True,"nb_cycle": 1},
                "PL" : {"puissance":1200 ,"intensity": 20,"usage_time": 0.75,"seq": False,"hc": True,"nb_cycle": 1},
                "FG_2" : {"puissance":300 ,"intensity": 3,"usage_time": 0.2,"seq": False,"hc": True,"nb_cycle": 4},
                "CE_2" : {"puissance":3000 ,"intensity": 15,"usage_time": 6,"seq": True,"hc": True,"nb_cycle": 1},
}

# data = [[True,True,True,True,True,True,False,True,True,True,True],
#         [True,True,True,True,True,True,False,True,True,True,False],
#         [True,True,True,True,True,True,False,True,True,False,False],
#         [True,True,False,True,True,True,True,True,True,False,True],
#         [True,True,True,True,True,True,False,True,True,False,False],
#         ]

def get_machine_time(time):
    res = []
    for _ in range(11):
        res.append([0]*48)

    for foyer in time:
        for index, machine in enumerate(foyer):
            for hr in machine:
                res[index][hr] += 1
    for machine in res:
        s =sum(machine)
        if s != 0:
            for k in range(len(machine)):
                machine[k] = machine[k] / s * 100

    return res

def print_time(t):
    s = ""
    for index, machine in enumerate(t):
        s += f"{index}\n"
        for hr in machine:
            s += f"{hr}, "
    return s


def compute_fit(t):
    d = 0
    mean = sum(t) / len(t)
    for e in t:
        d += abs(e - mean)
    return d

def compute_fit2(t):
    return max(t)


def random_main(data):
    particle = Popu(data)
    return compute_fit(particle.get_g_conso())
    # return compute_fit2(particle.get_g_conso())


def main(nb_part, nb_iter, data):
    mem = []

    particle = [Popu(data) for k in range(nb_part)]

    g_best = particle[0].get_data()
    g_conso = particle[0].get_g_conso()
    f = particle[0].fit 
    index = -1
    for i in range(len(particle)):
        if particle[i].fit < f:
            f = particle[i].fit
            index = i
    if index >=0 :
        g_best = particle[index].get_data()
        g_conso = particle[index].get_g_conso()

    o_g_conso = g_conso

    print("end init")
    
    for e in range(nb_iter):
        print(f"\n\n\nLOOP {e}")

        for p in particle:
            #update best pos
            p.update_best_pos()
        
        for p in particle:
            # Updatde speed and pos
            p.update(g_best,e)
            # compute new fit
            p.compute_fit()
            # p.compute_fit2()

        # update best gobal pos
        index = -1
        for i in range(len(particle)):
            if particle[i].fit < f:
                f = particle[i].fit
                index = i
        if index >= 0 :
            print("better found")
            g_conso = particle[index].get_g_conso()
            g_best = particle[index].get_data()
        
        with open("time_fit2_verif_consomax.txt", "w") as file:
            file.write(print_time(g_best))
            file.write("\n\nend\n\n")
        mem.append(compute_fit(g_conso))
        # mem.append(compute_fit2(g_conso))
 
    # print(g_conso)
    # print(g_best)
    return mem, g_best, g_conso

Foyer.set_hc(44, 13)
Foyer.set_static_data(machine_data)

N = 100
NB_ITER = 12
dataframe = pd.read_csv("data.csv", header=None)

# print(Foyer.machine_data)

print("PSO :")
mem, time_opti, conso_opti = main(20, NB_ITER, dataframe)
fig = plt.figure()
plt.plot(mem)
plt.xlabel("iteration")
plt.ylabel("fitness")
print(mem)

print("Random : ")
mem_rng = []
for i in range(10):
    if i % 10 == 0:
        print(i)
    mem_rng.append(random_main(dataframe))
print(sum(mem_rng)/ len(mem_rng))

machine_start = get_machine_time(time_opti)

fig, ax = plt.subplots(1)
ax.bar(range(48), conso_opti)

fig2, ax2 = plt.subplots(1)
for index, elem in enumerate(machine_start):
    ax2.plot(range(48), elem, label= f"Machine {index}")

plt.show()

