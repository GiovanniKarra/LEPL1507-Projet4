import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
import time
import scipy as sp
import pre_processing



# ----------------
#  PARAMETERS
# ----------------


#population = np.array([100, 200, 300, 400, 500])
#couverture = np.array([
    # [
    #     [0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
    #     [1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    #     [0, 0, 1, 1, 0, 1, 1, 0, 1, 0],
    #     [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    #     [1, 0, 0, 0, 0, 1, 1, 0, 0, 1]
    # ]



# ----------------
#  BASE MODEL
# ----------------

def basemodel(N_sat, N_villes, N_grid, population, couverture):
    """
    N_sat: nombre de satellites à placer
    N_villes: nombre de villes
    N_grid: nombre de positions possibles pour les satellites
    population: numpy array de taille N_villes contenant la population de chaque ville
    couverture: numpy array binaire de taille N_villes x N_grid contenant la couverture de chaque ville par chaque satellite:
                couverture[i][j] = 1 si ville i est couverte par satellite j, 0 sinon
    """

    
    # Variables
    y = cp.Variable(N_villes, name="y", boolean=True) # y[i] = 1 si ville i est couverte par un satellite, 0 sinon
    x = cp.Variable(N_grid, name="x", boolean=True)   # x[j] = 1 si satellite placé à la position j, 0 sinon

    # Objectif
    cout = cp.multiply(population, y) # population couverte (multiplication elementwise)
    objectif = cp.Maximize(cp.sum(cout)) # maximise la norme 1 (somme) des populations couvertes

    # Contraintes
    contraintes = []

    # N satellites
    contraintes.append(cp.sum(x) == N_sat)
    
    # Couverture
    for j in range(N_villes):
        vec_couverture = np.zeros(N_grid, dtype=bool)
        vec_couverture[couverture[j]] = True
        
        contraintes.append(y[j] <= cp.sum(cp.multiply(x, vec_couverture)))

    # Debug: voir si les contraintes respectent les DCP rules
    if verbose:
        for i in range(len(contraintes)):
            if not (contraintes[i].is_dcp()):
                print("Contrainte", i, "ne respecte pas DCP rules")


    # Solveur problème
    return cp.Problem(objectif, contraintes)

# -------------------

save_x = []
save_y = []
save_sol = []


for j in range(1):

    cities, grid = pre_processing.calc_grid("../geonames_be.csv", grid_size_X=30, grid_size_Y=30)

    # Function to generate the random array
    def generate_random_array(rows, columns):
        random_array = np.zeros((rows, columns), dtype=bool)
        for row in random_array:
            num_ones = np.random.randint(0, 200)  # At most 10 ones per row
            indices = np.random.choice(columns, num_ones, replace=False)
            row[indices] = True
        return random_array

    # Generate the random arrays
    #population = np.round(np.random.rand(N_villes)*100000)
    #sparse_array = np.random.randint(2, size=(N_villes, N_grid))
    #population = sp.sparse.csr_matrix(sparse_array)
    #couverture = generate_random_array(N_villes, N_grid)

    verbose = True
    N_sat = 4
    N_villes = len(cities)
    N_grid = len(grid) * len(grid[0])
    radius = 0.2

    population = [cities[i][2] for i in range(len(cities))]
    print(population)
    couverture = pre_processing.calc_adj(cities=cities, grid=grid, radius=radius)    

    problem = basemodel(N_sat, N_villes, N_grid, population, couverture)
    
    starttime = time.time()
    problem.solve(verbose=verbose, warm_start=True)
    endtime = time.time()

    vars = problem.variables()

    # Save variables
    for k in range(2):
        if vars[k].name() == "x":
            save_x.append(vars[k].value)
        elif vars[k].name() == "y":
            save_y.append(vars[k].value)

    save_sol.append(problem.value)
    

    print("\n=========== PROBLEME", j+1, "===========")
    #print("Population :", population)
    #print("Couverture :", couverture)
    print("Statut : %s" % problem.status)
    print("Population couverte : %d (%f %%)" % (problem.value, problem.value / np.sum(population) * 100))
    print("Temps d'exécution : %f sec (activer le mode verbose pour + de détails)" % (endtime - starttime))
    print("Variables x :", save_x[-1])


    for y in range(len(grid)):
        for x in range(len(grid[0])):
            plt.plot(grid[y][x][0], grid[y][x][1], "o", color="black", alpha=0.3)


    for i in range(len(cities)):
        plt.plot(cities[i][0], cities[i][1], "o", color="blue")


    sat_positions = np.array(save_x[-1])
    indices_sat_positions = np.where(sat_positions == 1)[0]
    for i in indices_sat_positions:
        y,x = pre_processing.index_to_grid(i, len(grid), len(grid[0]))
        plt.plot(grid[y][x][0], grid[y][x][1], "o", color="red")


    plt.show()
