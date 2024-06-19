AstroGlue
-----------------
AstroGlue serves as a bridge between the AstroLink clustering algorithm and the Glue visualization tool. 

AstroLink is a versatile clustering algorithm designed to extract meaningful hierarchical structures from astrophysical datasets. It has the capability to identify an arbitrary number of clusters with arbitrary shapes from user-defined data sets. The clustering structure can be visualized via the 2-dimensional AstroLink ordered-density plot.

Glue can be used to explore relationships within and among related datasets. Its features include - Linked Statistical Graphics, Flexible linking across data and Full scripting capability with Python. 

AstroGlue makes use of this very capability of Glue and links it with AstroLink with a Python tkinter-based GUI frontend. 

Installation
-----------------
The Python package AstroGlue can be installed from PyPI:


Basic Usage
-------------------
AstroGlue enables user to input either a .NPY file or a .CSV file containing astrophysical data (with multiple features like Position, Velocity, Abundances, etc). You can download a sample dataset (.NPY file) from the “data” folder.

Once a file is input, user can enter column names, choose the columns and the type of plot they wish to visualize on Glue. The may also choose to run AstroLink and can select various subsets of the dataset (called feature spaces). 

With these inputs, a GlueViz application window is automatically launched with the various necessary plots.

These inputs can be provided in two ways:

a) Using the tkinter GUI: 
---------
If the values of the variables are not input using the set_variables() method, a tkinter window 
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





