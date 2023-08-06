import nais_processor as nais
import aerosol_functions as af
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr


# Create a config file
nais.make_config_template("test.yml")

nais.nais_processor("config_clean.yml")

## ions
ds_clean = xr.open_dataset("./processed_clean/NAIS_20220720.nc")

neg_ions_clean = ds_clean.neg_ions.to_pandas()
pos_ions_clean = ds_clean.pos_ions.to_pandas()
neg_particles_clean = ds_clean.neg_particles.to_pandas()
pos_particles_clean = ds_clean.pos_particles.to_pandas()

ds_clean.close()

fig,ax = plt.subplots(4,1)
ax = ax.flatten()
af.plot_sumfile(neg_ions_clean,ax=ax[0],vmin=10,vmax=10000)
af.plot_sumfile(pos_ions_clean,ax=ax[1],vmin=10,vmax=10000)
af.plot_sumfile(neg_particles_clean,ax=ax[2],vmin=10,vmax=100000)
af.plot_sumfile(pos_particles_clean,ax=ax[3],vmin=10,vmax=100000)
plt.savefig("clean_data.png",bbox_inches="tight")
plt.close()
