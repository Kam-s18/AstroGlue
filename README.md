# Welcome to AstroGlue

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Kam-s18/AstroGlue/ci.yml?branch=main)](https://github.com/Kam-s18/AstroGlue/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/AstroGlue/badge/)](https://AstroGlue.readthedocs.io/)
[![codecov](https://codecov.io/gh/Kam-s18/AstroGlue/branch/main/graph/badge.svg)](https://codecov.io/gh/Kam-s18/AstroGlue)

AstroGlue serves as a bridge between the [AstroLink](https://github.com/william-h-oliver/astrolink) clustering algorithm and the [Glue](https://github.com/glue-viz/glue) visualization tool. 

AstroLink is a versatile clustering algorithm designed to extract meaningful hierarchical structures from astrophysical datasets. It has the capability to identify an arbitrary number of clusters with arbitrary shapes from user-defined data sets. The clustering structure can be visualized via the 2-dimensional AstroLink ordered-density plot.

Glue can be used to explore relationships within and among related datasets. Its features include - Linked Statistical Graphics, Flexible linking across data and Full scripting capability with Python. 

AstroGlue makes use of this very capability of Glue and links it with AstroLink with a Python tkinter-based GUI frontend.

## Installation

The Python package `AstroGlue` can be installed from PyPI:

```
python -m pip install AstroGlue
```
Basic Usage
-------------------
AstroGlue enables user to input either a .NPY file or a .CSV file containing astrophysical data (with multiple features like Position, Velocity, Abundances, etc). You can download a sample dataset (.NPY file) from the “data” folder.

Once a file is input, user can enter column names, choose the columns and the type of plot they wish to visualize on Glue. The may also choose to run AstroLink and can select various subsets of the dataset (called feature spaces). 

With these inputs, a GlueViz application window is automatically launched with the various necessary plots.

These inputs can be provided in two ways:

a) Using the tkinter GUI: 
---------
If the values of the variables are not input using the `set_variables()` method, a tkinter window 
is launched prompting the user to input all the variables required to run AstroLink and plot on Glue. 

Providing inputs through this method is quite straighforward and requires only the following lines of code:

```python
from AstroGlue import AstroGlue
astroglue = AstroGlue()
astroglue.run()
```

This opens up a tkinter GUI window that looks like this:

![image](https://github.com/Kam-s18/AstroGlue/assets/105807625/ddc2c1d7-187c-4a2c-acad-b4b6b2299966)

The user may now input a file of their choice (.CSV or .NPY), provide column names, choose plots that they wish to view and also run AstroLink (optionally) over various feature spaces:

![image](https://github.com/Kam-s18/AstroGlue/assets/105807625/d3849a38-c49f-4bf4-b00f-6ce6e809af3c)

Thereafter, clicking on the “Save Preferences and Start” button will initiate AstroLink clustering algorithm (if chosen to do so), prepare dataset and launch a Glue session with all the chosen plots and ordered-density plots from AtstroLink:

![image](https://github.com/Kam-s18/AstroGlue/assets/105807625/0a46a14b-8696-4b0c-8b09-b803eccd0680)

The user can select various subsets in any plot and visualize those data points in other plots. This feature enhances data analysis by providing deeper insights and facilitating more comprehensive comparisons:

![image](https://github.com/Kam-s18/AstroGlue/assets/105807625/79706ea7-48c2-4499-9c98-03b3ff91e892)

The following video explains the various features of this AstroGlue tkinter window that lets user to input all the required variables to run AstroLink and launch Glue with the chosen plots:
INSERT VIDEO HERE

b) Using set_variables() method:
--------------------------------------------
If the user already has the variables in python stirngs/lists, then `set_variables()` method can be used to input the variables into the AstroGlue class without having to use the GUI. This can be done with the following lines of code:

```python
file_path = "newhalo_young.csv" #Path to your npy or csv file (use // for absolute path)
data_df = pd.read_csv(file_path) # Your DataFrame initialization (use pd.read_csv or convert you numpy file to dataframe with column names)
feature_spaces = [["x", "y", "z"],["vx", "vy", "vz"],["x", "y", "z","vx", "vy", "vz"]] # Your list of feature spaces
adaptive_list = [0,0,1] # Your list of adaptive parameters
k_den_list = [20,20,20]  # Your list of k_den parameters
S_list = ['auto','auto','auto']  # Your list of S parameters
k_link_list = ['auto','auto','auto']  # Your list of k_link parameters
h_style_list = [1,1,1]  # Your list of h_style parameters
workers_list = [-1,-1,-1]  # Your list of workers parameters
verbose_list = [0,0,0]  # Your list of verbose parameters
feature_space_name = ["pos","vel","posvel"]  # Your list of feature space names
var_plot_list = [["x", "y", "z"],["vx","vy","vz"],["Fe/H","Alpha/Fe"]]  # Your list of variable plots
type_l = ["3D Scatter Plot","3D Scatter Plot","2D Scatter Plot (rectilinear)"]  # Your list of plot types

# Initialize AstroGlue instance
astroglue = AstroGlue()
# Set variables
astroglue.set_variables(file_path, data_df, feature_spaces, adaptive_list, k_den_list, S_list, k_link_list, h_style_list, workers_list, verbose_list, feature_space_name, var_plot_list, type_l)
astroglue.run()
```

This would run the astrolink clustering algorithm and launch a Glue window with the required plots as in the previous example. If the user does not wish to run the astrolink algorithm, the feature_spaces can be declared as an empty list.

## Development installation

If you want to contribute to the development of `AstroGlue`, we recommend
the following editable installation from this repository:

```
git clone https://github.com/Kam-s18/AstroGlue
cd AstroGlue
python -m pip install --editable .[tests]
```

Having done so, the test suite can be run using `pytest`:

```
python -m pytest
```

## Acknowledgments

This repository was set up using the [SSC Cookiecutter for Python Packages](https://github.com/ssciwr/cookiecutter-python-package).
