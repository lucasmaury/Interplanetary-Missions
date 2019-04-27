#!/usr/bin/env python
# coding: utf-8

# Import des librairies

# In[67]:


import pygmo as pg
import pykep as pk
#from pykep import *
from matplotlib import pyplot as plt


# Partie 1 : Transfert direct

# Encounter sequence.

# In[68]:


seq = [pk.planet.jpl_lp('earth'),pk.planet.jpl_lp('mars')]
print (seq)


# Position des planètes et orbites

# In[69]:


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.gca(projection='3d')
e = pk.epoch_from_string('2019-07-27 17:09:54') #date du jour
pk.orbit_plots.plot_planet(seq[0], e, color = 'b', legend=True, ax=ax)
pk.orbit_plots.plot_planet(seq[1], e, color = 'r', legend=True, ax=ax)
plt.show()


# Launch windonws, time of flight and departure vinf

# In[70]:


#comment sont choisis ces limites ?
t0 = [e,pk.epoch(10000)]
#t0 = [epoch(4000),epoch(10000)]
tof = [60,380] 
vinf = [0,4] #fonction du launcher
print (t0)


# Definition du probleme d'optimisation global

# In[71]:


Mga_1dsm = pk.trajopt.mga_1dsm()
prob = pk.trajopt.mga_1dsm(seq = seq, t0 = t0, tof = tof, vinf = vinf)
pg.problem(prob)


# Randomly generated solution

# In[72]:


pop = pg.population(prob,1)
ax = prob.plot(pop.champion_x)
plt.show()
print (prob.pretty(pop.champion_x))


# Evolution et inspection d'une bonne solution

# In[73]:


algo = pg.algorithm(pg.cmaes(gen = 2500, force_bounds = True))
# sans force_bounds = True j'obtenais des erreurs
l = list()
for i in range (10) : 
    pop = pg.population(prob,10)
    pop = algo.evolve(pop)
    print (pop.champion_f)
    l.append((pop.champion_f,pop.champion_x))
l = sorted(l, key = lambda x: x[0])
print (l)
print (l[0])


# In[74]:


print (prob.pretty(l[0][1]))


# In[75]:


prob.plot(l[0][1])
plt.show()


# Partie 2 : Utilisation de fly-bys

# In[89]:


seq_fb = [pk.planet.jpl_lp('earth'),pk.planet.jpl_lp('venus'),pk.planet.jpl_lp('earth'),pk.planet.jpl_lp('mars')]


# In[90]:


t0_fb = [e, pk.epoch(10000)]
#Time of flight for the three legs: how the bounds are defined ?
tof_fb = [1,1800]
#vinf is the same


# In[101]:


traj_fb = pk.trajopt.mga_1dsm(seq = seq_fb, t0 = t0_fb, tof = tof_fb, vinf = vinf)
prob_fb = pg.problem(traj_fb)

#Can we set the time of flight for each legs ? Does not seem to work when I tried


# In[102]:


pop_fb = pg.population(prob_fb,1)
ax_fb = traj_fb.plot(pop_fb.champion_x)
plt.show()
print (traj_fb.pretty(pop_fb.champion_x))


# In[106]:


algo_fb = pg.algorithm(pg.sade(gen = 500))
l = list()
for i in range (10) : 
    pop_fb = pg.population(prob_fb,20)
    pop_fb = algo.evolve(pop_fb)
    print (pop_fb.champion_f)
    l.append((pop_fb.champion_f,pop_fb.champion_x))
l = sorted(l, key = lambda x: x[0])


# Comments: 

# Using a different solution technique: pygmo's arichipelago/island

# In[96]:


algo_fb = pg.algorithm(pg.sade(gen = 200))
l = list()
for i in range (10) : 
    archi = pg.archipelago(n = 16, algo = algo_fb, prob = prob_fb, pop_size = 8, seed = 20)
    archi.evolve(15)
    best_island = sorted(archi, key = lambda x: x.get_population().champion_f[0])[0]
    l.append((best_island.get_population().champion_f,best_island.get_population().champion_x))
    print (best_island.get_population().champion_f[0])
l = sorted(l, key = lambda x: x[0])


# In[103]:


print (traj_fb.pretty(l[0][1]))


# Lauch date around 8000 MJD2000, so we restrict the launch date around that point and run the optimization again

# In[105]:


t0_fb = [pk.epoch(7700), pk.epoch(8300)]
tof_fb = [1,1800]
traj_fb = pk.trajopt.mga_1dsm(seq = seq_fb, t0 = t0_fb, tof = tof_fb, vinf = vinf)
prob_fb = pg.problem(traj_fb)
algo_fb = pg.algorithm(pg.sade(gen = 200))
l = list()
for i in range (10) : 
    archi = pg.archipelago(n = 16, algo = algo_fb, prob = prob_fb, pop_size = 8, seed = 20)
    archi.evolve(15)
    best_island = sorted(archi, key = lambda x: x.get_population().champion_f[0])[0]
    l.append((best_island.get_population().champion_f,best_island.get_population().champion_x))
    print (best_island.get_population().champion_f[0])
l = sorted(l, key = lambda x: x[0])


# In[ ]:




