from BENCH_spherical_satellites_repartition import *


def sat_couv():
    file = "../refactored_smol.csv"
    data = pd.read_csv(file)
    tot_popu = data["size"].sum()
    sols_cont = []
    sols_disc = []
    sats = np.logspace(1,2.7,num=15,dtype=int)
    for i in range(len(sats)):
        print("#"*20)
        print("Satellites:", sats[i])
        print("#"*20)
        out = spherical_satellites_repartition(sats[i], file)
        sols_cont.append(100*out[1]/tot_popu)
        sols_disc.append(100*out[2]/tot_popu)
            
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
    ray = np.logspace(1,3,num=10,dtype=int)
    
    for i in range(len(ray)):
        print("#"*20)
        print("radius:", ray[i])
        print("#"*20)
        rad = np.sqrt((ray[i]/6371)**2+0.2**2)
        out = spherical_satellites_repartition(100, file, radius_acceptable=rad)
        sols_cont.append(100*out[1]/tot_popu)
        sols_disc.append(100*out[2]/tot_popu)
            
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
    grid = np.logspace(1,3.8,num=30,dtype=int)
    
    for i in range(len(grid)):
        print("#"*20)
        print("size grid:", grid[i])
        print("#"*20)
        out = spherical_satellites_repartition(100, file, grid_size=grid[i])
        sols_cont.append(100*out[1]/tot_popu)
        sols_disc.append(100*out[2]/tot_popu)
        delta.append(100*(out[1]-out[2])/tot_popu)
    
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
    
def grid_time():
    file = "../refactored_smol.csv"
    time_cont = []
    time_disc = []
    time_pre = []
    time_tot = []
    width = []
    grid = np.logspace(2,4.3,num=20,dtype=int)
    
    for i in range(len(grid)):
        print("#"*20)
        print("size grid:", grid[i])
        print("#"*20)
        out = spherical_satellites_repartition(100, file, grid_size=grid[i])
        width.append(grid[i]/10)
        time_tot.append(out[6]-out[3]-out[4]-out[5])
        time_cont.append(out[5])
        time_disc.append(out[4])
        time_pre.append(out[3])
        
    
    plt.bar(grid, time_pre, label="preprocessing time", width=width)
    plt.bar(grid, time_disc, label="discrete solver time", bottom=time_pre,width=width)
    plt.bar(grid, time_cont, label="continuous solver time", bottom=np.add(time_pre,time_disc),width=width)
    plt.bar(grid, time_tot, label="total time", bottom=np.add(time_pre,np.add(time_disc,time_cont)) ,width=width)
    plt.xlabel("Size of the grid")
    plt.ylabel("Time (s)")
    plt.title("Time as a function of the size of the grid")
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    # plt.savefig("../images/grid_time.pdf")
    plt.show()
    
def sat_time():
    file = "../refactored_smol.csv"
    time_cont = []
    time_disc = []
    time_pre = []
    time_tot = []
    width = []
    sat = np.logspace(1,2.7,num=20,dtype=int)
    
    for i in range(len(sat)):
        print("#"*20)
        print("number of satellites:", sat[i])
        print("#"*20)
        out = spherical_satellites_repartition(sat[i], file)
        width.append(sat[i]/10)
        time_tot.append(out[6]-out[3]-out[4]-out[5])
        time_cont.append(out[5])
        time_disc.append(out[4])
        time_pre.append(out[3])
        
    
    plt.bar(sat, time_pre, label="preprocessing time", width=width)
    plt.bar(sat, time_disc, label="discrete solver time", bottom=time_pre,width=width)
    plt.bar(sat, time_cont, label="continuous solver time", bottom=np.add(time_pre,time_disc),width=width)
    plt.bar(sat, time_tot, label="total time", bottom=np.add(time_pre,np.add(time_disc,time_cont)) ,width=width)
    plt.xlabel("number of satellites")
    plt.ylabel("Time (s)")
    plt.title("Time as a function of the number of satellites")
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    # plt.savefig("../images/sat_time.pdf")
    plt.show()
    
def villes_time():
    file = "../refactored_cleared.csv"
    time_cont = []
    time_disc = []
    time_pre = []
    time_tot = []
    width = []
    villes = np.logspace(1,4,num=20,dtype=int)
    
    for i in range(len(villes)):
        print("#"*20)
        print("number of cities:", villes[i])
        print("#"*20)
        out = spherical_satellites_repartition(100, file, nb_cities=villes[i])
        width.append(villes[i]/10)
        time_tot.append(out[6]-out[3]-out[4]-out[5])
        time_cont.append(out[5])
        time_disc.append(out[4])
        time_pre.append(out[3])
        
    
    plt.bar(villes, time_pre, label="preprocessing time", width=width)
    plt.bar(villes, time_disc, label="discrete solver time", bottom=time_pre,width=width)
    plt.bar(villes, time_cont, label="continuous solver time", bottom=np.add(time_pre,time_disc),width=width)
    plt.bar(villes, time_tot, label="total time", bottom=np.add(time_pre,np.add(time_disc,time_cont)) ,width=width)
    plt.xlabel("number of cities")
    plt.ylabel("Time (s)")
    plt.title("Time as a function of the number of cities")
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    # plt.savefig("../images/villes_time.pdf")
    plt.show()
    
if __name__ == "__main__":
    t0 = time.perf_counter()
    # sat_couv()
    # ray_couv()
    # grid_couv()
    # grid_time()
    # sat_time()  
    # villes_time()
    print("Time to solve:", time.perf_counter() - t0)