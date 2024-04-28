import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
import time
import scipy as sp
import pre_processing


# ----------------
#  BASE MODEL
# ----------------

def basemodel(N_sat, N_cities, N_grid, population, coverage, verbose=False):
    """
    N_sat:      number of satellites to place
    N_cities:   number of cities
    N_grid:     number of grid points (possible satellite positions)
    population: numpy array of size N_cities containing the population of each city
    coverage:   binary numpy array of size N_cities x N_grid containing the coverage of each city by each satellite:
                coverage[i][j] == 1 if city i is covered by satellite j, 0 otherwise
    """
    
    # Variables
    y = cp.Variable(N_cities, name="y", boolean=True) # y[i] = 1 si ville i est couverte par un satellite, 0 sinon
    x = cp.Variable(N_grid, name="x", boolean=True)   # x[j] = 1 si satellite placé à la position j, 0 sinon

    # Objectif
    cout = cp.multiply(population, y) # population couverte (multiplication elementwise)
    objectif = cp.Maximize(cp.sum(cout)) # maximise la norme 1 (somme) des populations couvertes

    # Contraintes
    contraintes = []

    # N satellites
    contraintes.append(cp.sum(x) <= N_sat)
    
    # Couverture
    for i in range(N_cities):
        vec_couverture = np.zeros(N_grid, dtype=bool)
        vec_couverture[coverage[i]] = True
        
        contraintes.append(y[i] <= cp.sum(cp.multiply(x, vec_couverture)))

    # Debug: voir si les contraintes respectent les DCP rules
    if verbose:
        for i in range(len(contraintes)):
            if not (contraintes[i].is_dcp()):
                print("Contrainte", i, "ne respecte pas DCP rules")

    # Solveur problème
    return cp.Problem(objectif, contraintes)

# -------------------

if __name__ == "__main__":
	data_names = ["../geonames_be.csv"]   # <-- Mettre ici les noms des fichiers csv à tester
	N_experiences = len(data_names)

	verbose = True
	N_sat = 6
	radius = 0.4
	grid_size_X = 30
	grid_size_Y = 30


	save_x = []
	save_y = []
	save_sol = []

	for j in range(N_experiences):

		cities, grid = pre_processing.calc_grid(data_names[j], grid_size_X, grid_size_Y)
		N_cities = len(cities)
		N_grid = len(grid) * len(grid[0])

		population = [cities[i][2] for i in range(len(cities))]

		startpre = time.time()
		covered_adj = pre_processing.calc_adj(cities=cities, grid=grid, radius=radius)  
		endpre = time.time()  

		problem = basemodel(N_sat, N_cities, N_grid, population, covered_adj)
		
		startsolve = time.time()
		problem.solve(verbose=verbose, warm_start=True)
		endsolve = time.time()

		vars = problem.variables()

		# Save variables
		for k in range(2):
			if vars[k].name() == "x":
				save_x.append(vars[k].value)
			elif vars[k].name() == "y":
				save_y.append(vars[k].value)

		save_sol.append(problem.value)
		
		if verbose:
			print("\n=========== PROBLEME", j+1, "===========")
			#print("Population :", population)
			#print("Couverture :", coverage)
			print("Statut : %s" % problem.status)
			print("Population couverte : %d (%f %%)" % (problem.value, problem.value / np.sum(population) * 100))
			print("Temps de solve : %f sec" % (endsolve - startsolve))
			#print("Variables x :", save_x[-1])

		for y in range(len(grid)):
			for x in range(len(grid[0])):
				plt.plot(grid[y][x][0], grid[y][x][1], "o", color="black", alpha=0.3)


		for i in range(len(cities)):
			plt.plot(cities[i][0], cities[i][1], "o", color="blue", alpha=0.6)

		
		sat_positions = np.array(save_x[-1])
		indices_sat_positions = np.where(sat_positions > 1-1e-3)[0]
		print("Positions satellites (id grid) :", indices_sat_positions)
		for i in indices_sat_positions:
			y,x = pre_processing.index_to_grid(i, len(grid), len(grid[0]))
			plt.plot(grid[y][x][0], grid[y][x][1], "*", color="red", markersize=10)
			circle = plt.Circle((grid[y][x][0], grid[y][x][1]), radius, color='r', fill=False, linestyle="--", zorder=2)
			plt.gca().add_patch(circle)


		plt.show()
