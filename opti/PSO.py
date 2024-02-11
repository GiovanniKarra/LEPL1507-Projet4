"""
    Solving Maximal Covering Location Problem with Particle Swarm Optimisation (PSO)
    Inspired by: 
    https://www.researchgate.net/publication/286019467_Solving_Maximal_Covering_Location_with_Particle_Swarm_Optimization



"""

import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt

# import numba


class pos:
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y
        pass

    def __add__(self, other):
        return pos(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return pos(self.x - other.x, self.y - other.y)
    
    def __mul__(self, sclar: float):
        return pos(self.x * sclar, self.y * sclar)
    


class Particle:
    c1 = 1
    c2 = 1
    fit = 0
    radius = 1

    def __init__(self, n: int, minPOS: pos, maxPOS: pos) -> None:
        self.s = np.empty(n, dtype=pos) # Vecteur des positons de chaque particule
        self.v = np.empty(n, dtype=pos) # Vecteur des vitesse de chaque particule
        self.pbest = np.empty(n, dtype=pos)

        self.n = n                      # In our context, the number of satellite to place 
        self.r1 = random.uniform(0, 1) * self.c1
        self.r2 = random.uniform(0, 1) * self.c2
        self.maxPOS = maxPOS
        self.minPOS = minPOS

        # Intialise the random starting position on the rectangle
        for i in range(n):
            self.s[i] = pos(random.uniform(minPOS.x, maxPOS.x), random.uniform(minPOS.y, maxPOS.y))
            self.v[i] = pos(0, 0)


    def update(self, gbest: np.ndarray ,w: float) -> None:
        for i in range(self.n):

            tempV = self.v[i] * w + (self.pbest[i] - self.s[i]) * self.r1 + (gbest[i] - self.s[i]) * self.r2

            if tempV.x > maxPOS.x: tempV.x = maxPOS.x
            if tempV.x < -maxPOS.x: tempV.x = -maxPOS.x

            if tempV.y > maxPOS.y: tempV.y = maxPOS.y
            if tempV.y < - maxPOS.y: tempV.y =  -maxPOS.y

            
            self.v[i] = tempV
            tempS = self.v[i] + self.s[i]


            if tempS.x > maxPOS.x: tempS.x = maxPOS.x
            if tempS.x < minPOS.x: tempV.x = minPOS.x

            if tempS.y > maxPOS.y: tempS.y = maxPOS.y
            if tempS.y < minPOS.y: tempS.y = minPOS.y

         
        
            self.s[i] = tempS


    def update_pbest(self, fit: float):
        self.fit = fit
        for i in range(self.n):
            self.pbest[i] = self.s[i]


    def fitness(self, cities: np.ndarray) -> float:
        """
        @pre:
            cities: tuple(x, y, weight)
        @post:
            return a score on how good is the current satellite position.
        """
        temp = 0.0

        cover = np.zeros(len(cities))


        for c in range(len(cities)):
            if cover[c] == 0:
                for i in range(self.n):

                    if self.radius >= np.sqrt((cities[c][0] - self.s[i].x) ** 2 + (cities[c][1] - self.s[i].y) ** 2) and cover[c] != 1:
                        temp += cities[c][2]
                        cover[c] = 1

        return temp
        





def PSO(minPOS: pos, maxPOS: pos, cities: np.ndarray, nb_sat: int, nb_particule = 100, k_max = 1000) -> np.ndarray:
    """
    @pre:
        minPOS: minimal position of satellites in coordinates (x,y)
        maxPOS: maximal position of satellites in coordinates (x,y)
        cities: array of tuple (x, y, weight)
        nb_sat: nb of satellites used
        nb_particules: number of the particule in the simulation
        k_max: maximal nb of iteration

    @post:
        return the best solution found during the k iterations
    
    """
    
    best_pbest = 0
    gbest = np.empty(nb_sat, dtype=pos)

    # Intialisation
    particules = np.empty(nb_particule, dtype=Particle)
    for i in range(nb_particule):
        particules[i] = Particle(nb_sat, minPOS, maxPOS)
        fit_score = particules[i].fitness(cities)
        
        if fit_score >= best_pbest:
            gbest = particules[i].s
            best_pbest = fit_score

        particules[i].update_pbest(fit_score)

    w = lambda k : 0.9 - (0.5/k_max) * k

    for k in range(k_max):

        w_k = w(k)

        for p in particules:

            fit_score = p.fitness(cities)

            if fit_score > p.fit:
                p.update_pbest(fit_score)

            if p.fit > best_pbest:
                gbest = p.s
                best_pbest = p.fit


        for p in particules:
            p.update(gbest, w_k)


    return (gbest, best_pbest)




if __name__ == "__main__":
    random.seed(0)
    data_be_smol : pd.DataFrame = pd.read_csv("../geonames_be.csv", sep=";")
    
    cities = np.empty(len(data_be_smol), tuple)
    tot_population = 0

    for i in range(len(cities)):
        coor = data_be_smol["Coordinates"][i].split(",")
        y  = float(coor[0])
        x = float(coor[1])
        weight =  float(data_be_smol["Population"][i])
        tot_population += weight

        cities[i] = (x, y,weight)
        plt.plot(x, y, "o", color="blue")
        name = data_be_smol["Name"][i]
        # plt.text(x, y, name)


    print(cities)
    
    
    minPOS = pos(0, 40)
    maxPOS = pos(7, 60)

    (best, score) = PSO(minPOS, maxPOS, cities, nb_sat=2, nb_particule=50, k_max=20)

    print("Percent of the population covered: ", score/tot_population * 100)
    

    print()
    print()
    print()

    for i in range(len(best)):
        print(best[i].x, best[i].y)
        plt.plot(best[i].x, best[i].y, "o", color="r")
        radius = plt.Circle((best[i].x, best[i].y), 1, color="g")
        plt.gca().add_patch(radius)


    
    plt.show()
    
    









