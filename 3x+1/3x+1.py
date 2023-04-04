from random import randint
# import matplotlib.pyplot as plt

###### PARAMETERS #####
nInterval_a = 1 
nInterval_b = 10000
graph_count = 1000
###### PARAMETERS #####

y_s, n_memory = [], []
for _ in range(graph_count):
    y = []

    n = randint(nInterval_a, nInterval_b)
    while n in n_memory: n = randint(nInterval_a, nInterval_b)
    n_memory += [n]

    y += [n]
    while n != 1:  
        if n % 2 == 0:
            n /= 2
            y += [n]
        else:
            n = 3*n + 1
            y += [n]    
    y_s += [y]
        
# for y in y_s: plt.plot(y)
# plt.show()

from os import system
system('pip install plotly')
import plotly.graph_objs as go

fig = go.Figure()
for y in y_s: fig.add_trace(go.Scatter(y=y))
fig.show()