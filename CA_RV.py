import numpy as np
import scipy as sp
import scipy.sparse

print("Numpy version {}".format(np.__version__))

import matplotlib as mpl
import matplotlib.pyplot as plt # Core plotting support
print("Matplotlib version {}".format(mpl.__version__))

def empty_world(x, n=None):
    from numpy import ndarray
    if isinstance(x, ndarray):
        return np.zeros(x.shape)
    m = x
    if n is None:
        n = m
    return np.zeros((m+2, n+2))

def interior(W, dx=0, dy=0):
    m, n = W.shape
    return W[(1+dy):(m-1+dy), (1+dx):(n-1+dx)]
    
def create_world(n, q):
    World = empty_world(n)
    Interior = interior(World)
    Interior[:, :] = np.random.choice([0, 1], p=[1-q, q], size=(n, n))
    return World

def is_dead(W):
    return W == 0

def is_alive(W):
    return W == 1

def count(W, cond_fun):
    return cond_fun(W).sum()

def summarize_world(W):
    m, n = W.shape[0]-2, W.shape[1]-2
    n_alive = count(interior(W), is_alive)
    n_dead = count(interior(W), is_dead)
    print(f"The world is {m} x {n} in size (excluding padded boundaries).")
    print(f"{n_alive} cells are alive, the remaining {n_dead} are not.")

def show_world(W, title=None, **args):
    if 'cmap' not in args:
        args['cmap'] = 'jet'
    if 'vmin' not in args and 'vmax' not in args:
        args['vmin'] = 0
        args['vmax'] = 3
    plt.figure(figsize=(8, 8))
    plt.matshow(W, fignum=1, **args)
    plt.xlabel('column')
    plt.ylabel('row')
    plt.colorbar()
    if title is None:
        m, n = W.shape[0]-2, W.shape[1]-2
        n_alive = count(interior(W), is_alive)
        n_dead = count(interior(W), is_dead)
        percent_alive = n_alive / (n_alive + n_dead) * 1e2
        title = f'{m} x {n}: {n_alive} alive, {n_dead} not so much ($\\approx$ {percent_alive:.1f}%)'
    plt.title(title)
    pass

# Demo:
World = create_world(20, 0.25)
summarize_world(World)
show_world(World)

def count_neighbors(W, exclude_center=False):
    C = empty_world(W)
    C_int = interior(C)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if exclude_center and (dx, dy) == (0, 0):
                continue
            C_int += interior(W, dx=dx, dy=dy)
    return C

def evolve(W):
    W_new = W.copy()
    Alive = is_alive(W)
    Dead = is_dead(W)
    N = count_neighbors(W, exclude_center=True) # living neighbors
    
    W_new_int = interior(W_new)
    N_int = interior(N)
    W_new_int[:, :] = (interior(Alive) & ((N_int == 2) | (N_int == 3))) \
                      | (interior(Dead) & (N_int == 3))
    return W_new

# Demo:
World_next = evolve(World)
show_world(World_next)
summarize_world(World_next)