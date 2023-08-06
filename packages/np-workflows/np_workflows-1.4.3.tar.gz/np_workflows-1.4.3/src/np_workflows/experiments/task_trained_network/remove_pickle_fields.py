#%% 
import pathlib
import pickle

p = pathlib.Path("//allen/programs/mindscope/workgroups/np-exp/1253554040_366122_20230312/1253554040_366122_20230312.stim.pkl")
data = pickle.loads(p.read_bytes(), encoding='latin1')

d = {}

for key in ('sweep_frames', 'sweep_order', 'frame_list'):
    d[key] = {idx: stim[key] for idx, stim in enumerate(data['stimuli'])}
    

for _ in data['stimuli']:
    del _['sweep_frames']
    del _['sweep_order']
    del _['frame_list']
    
p.with_stem(p.stem + '-sweep_frames-sweep_order-frame_list-removed').write_bytes(pickle.dumps(data, protocol=2))

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

# %% Sweep frames - arrays of tuples [(1,2), (3,4), (5,6), ...)]
ax, fig = plt.subplots()
sf = []
for _ in d['sweep_frames'][0]:
    sf.extend(_)
# plt.plot(sf)
plt.plot(sf)
fig.set_xlim(0, 2)
fig.set_ylim(0, 4)

# %%
ax, fig = plt.subplots()
x = plt.plot(*_ for _ in d['sweep_frames'][0])


# %%
ax, fig = plt.subplots()
for _ in d['sweep_order']:
    plt.plot(d['sweep_order'][_])
    
# %%
ax, fig = plt.subplots()
for _ in d['frame_list']:
    plt.plot(d['frame_list'][_])
    
# %%
ax, fig = plt.subplots()
plt.plot(d['frame_list'][6])


# %%
p_2 = pathlib.Path("//allen/programs/mindscope/workgroups/np-exp/1250977899_366122_20230301/1250977899_366122_20230301.stim.pkl")
data_2 = pickle.loads(p.read_bytes(), encoding='latin1')

d_2 = {}

for key in ('sweep_frames', 'sweep_order', 'frame_list'):
    d_2[key] = {idx: stim[key] for idx, stim in enumerate(data['stimuli'])}
    
# %%

for _ in data['stimuli']:
    del _['sweep_frames']
    del _['sweep_order']

# %%
p.with_stem(p.stem + '-sweep_frames-sweep_order-removed').write_bytes(pickle.dumps(data, protocol=2))
# %%
for _ in data['stimuli']:
    del _['frame_list']
    
p.with_stem(p.stem + '-sweep_frames-sweep_order-frame_list-removed').write_bytes(pickle.dumps(data, protocol=2))