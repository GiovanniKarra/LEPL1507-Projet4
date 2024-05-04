from BENCH_spherical_satellites_repartition import *


def sat_couv():
    file = "../refactored_smol.csv"
    data = pd.read_csv(file)
    tot_popu = data["size"].sum()
    sols_cont = []
    sols_disc = []
    sats = []
    for i in range(1,10):
        garb, sol_cont, sol_disc = spherical_satellites_repartition(i*10, file)
        sols_cont.append(100*sol_cont/tot_popu)
        sols_disc.append(100*sol_disc/tot_popu)
        sats.append(i*10)
        print("#"*20)
        print("Satellites:", i*10)
        print("#"*20)
        
    for i in range(1,6):
        garb, sol_cont, sol_disc = spherical_satellites_repartition(i*100, file)
        sols_cont.append(100*sol_cont/tot_popu)
        sols_disc.append(100*sol_disc/tot_popu)
        sats.append(i*100)
        print("#"*20)
        print("Satellites:", i*100)
        print("#"*20)
            
    plt.plot(sats, sols_cont, label="result with continuous solver")
    plt.plot(sats, sols_disc, label="result with discrete solver")
    plt.xlabel("Number of satellites")
    plt.ylabel("Coverage (%)")
    plt.title("Coverage as a function of the number of satellites")
    plt.xscale("log")
    plt.legend()
    # plt.savefig("../images/sat_couv.pdf")
    plt.show()
    
def ray_couv():
    file = "../refactored_smol.csv"
    data = pd.read_csv(file)
    tot_popu = data["size"].sum()
    sols_cont = []
    sols_disc = []
    ray = []
    
    for i in range(1,10):
        rad = np.sqrt((10*i/6371)**2+0.2**2)
        garb, sol_cont, sol_disc = spherical_satellites_repartition(100, file, radius_acceptable=rad)
        sols_cont.append(100*sol_cont/tot_popu)
        sols_disc.append(100*sol_disc/tot_popu)
        ray.append(i*10)
        print("#"*20)
        print("radius:", i*10)
        print("#"*20)
    
    for i in range(1,11):
        rad = np.sqrt((100*i/6371)**2+0.2**2)
        garb, sol_cont, sol_disc = spherical_satellites_repartition(100, file, radius_acceptable=rad)
        sols_cont.append(100*sol_cont/tot_popu)
        sols_disc.append(100*sol_disc/tot_popu)
        ray.append(i*100)
        print("#"*20)
        print("radius:", i*100)
        print("#"*20)
            
    plt.plot(ray, sols_cont, label="result with continuous solver")
    plt.plot(ray, sols_disc, label="result with discrete solver")
    plt.xlabel("radius (km)")
    plt.ylabel("Coverage (%)")
    plt.title("Coverage as a function of the acceptable radius")
    plt.xscale("log")
    plt.legend()
    # plt.savefig("../images/ray_couv.pdf")
    plt.show()
    
def grid_couv():
    file = "../refactored_smol.csv"
    data = pd.read_csv(file)
    tot_popu = data["size"].sum()
    sols_cont = []
    sols_disc = []
    delta = []
    grid = []
    
    for i in range(0,301,10):
        if i == 0:
            i = 1
        garb, sol_cont, sol_disc = spherical_satellites_repartition(100, file, grid_size=i*100)
        sols_cont.append(100*sol_cont/tot_popu)
        sols_disc.append(100*sol_disc/tot_popu)
        delta.append(100*(sol_cont-sol_disc)/tot_popu)
        grid.append(i*100)
        print("#"*20)
        print("size grid:", i*100)
        print("#"*20)
    
    plt.plot(grid, sols_cont, label="result with continuous solver")
    plt.plot(grid, sols_disc, label="result with discrete solver")
    plt.xlabel("Size of the grid")
    plt.ylabel("Coverage (%)")
    plt.title("Coverage as a function of the size of the grid")
    plt.xscale("log")
    plt.legend()
    # plt.savefig("../images/grid_couv.pdf")
    plt.show()   
    
    plt.plot(grid, delta, label="delta between continuous solver and discrete solver")
    plt.xlabel("Size of the grid")
    plt.ylabel("Delta of coverage (%)")
    plt.title("Coverage as a function of the size of the grid")
    plt.xscale("log")
    plt.legend()
    # plt.savefig("../images/grid_delta_couv.pdf")
    plt.show()   
    
    
if __name__ == "__main__":
    t0 = time.perf_counter()
    # sat_couv()
    # ray_couv()
    grid_couv()
    print("Time to solve:", time.perf_counter() - t0)