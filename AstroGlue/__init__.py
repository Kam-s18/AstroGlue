# The version file is generated automatically by setuptools_scm
from AstroGlue._version import version as __version__
from .AstroGlue import AstroGlue
import pandas as pd
  
file_path = "../data/newhalo_young.csv" #Path to your npy or csv file (use //)
data_df = pd.read_csv(file_path) # Your DataFrame initialization (use pd.read_csv or convert you numpy file to dataframe with column names)
feature_spaces = [["x (kpc)", "y (kpc)", "z (kpc)"],["vx", "vy", "vz"]] # Your list of feature spaces
adaptive_list = [0,0] # Your list of adaptive parameters
k_den_list = [20,20]  # Your list of k_den parameters
S_list = ['auto','auto']  # Your list of S parameters
k_link_list = ['auto','auto']  # Your list of k_link parameters
h_style_list = [1,1]  # Your list of h_style parameters
workers_list = [-1,-1]  # Your list of workers parameters
verbose_list = [0,0]  # Your list of verbose parameters
feature_space_name = ["pos","vel"]  # Your list of feature space names
var_plot_list = [["x (kpc)", "y (kpc)", "z (kpc)"],["vx","vy","vz"],["Fe/H","Alpha/Fe"]]  # Your list of variable plots
type_l = ["3D Scatter Plot","3D Scatter Plot","2D Scatter Plot (rectilinear)"]  # Your list of plot types

# Initialize AstroGlue instance
astroglue = AstroGlue()

# Set variables
astroglue.set_variables(file_path, data_df, feature_spaces, adaptive_list, k_den_list, S_list, k_link_list,
                        h_style_list, workers_list, verbose_list, feature_space_name, var_plot_list, type_l)

astroglue.run()

