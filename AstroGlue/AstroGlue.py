#Importing necessary libraries
import numpy as np
import pandas as pd
from glue.core import DataCollection
from glue_qt.app.application import GlueApplication
from glue_qt.viewers.scatter import ScatterViewer
from glue_vispy_viewers.scatter.scatter_viewer import VispyScatterViewer
from glue_qt.viewers.histogram import HistogramViewer
from astrolink import AstroLink
import tkinter as tk
from tkinter import *
from tkinter import filedialog, Scrollbar, Canvas
from tkinter import ttk
import webbrowser
import re
import os.path

class AstroGlue:
    """AstroGlue acts as a bridge between AstroLink clustering algorithm and GlueViz data visualization package. 

    It enables user to input either a .NPY file or a .CSV file containing galaxy data and has multiple features like
    Positions, Velocity, Abundances, etc. Once a file is imported, user can enter column names, choose the columns
    and the type of plot they wish to analyse on GlueViz. The user may also choose to run AstroLink and can select various
    subsets of the dataset for AstroLink to run on (feature spaces). 
    
    These inputs can be provided in two ways:
    a) Using the tkinter GUI: If the values of the variables are not input using the set_variables() method, a tkinter window 
    is launched prompting the user to input all the variables required to run AstroLink and plot on GlueViz

    b) Using set_variables() method: If the user already has the variables in python stirngs/lists, then set_variables() method
    can be used to input the variables into the AstroGlue class without having to use the GUI.

    Once these inputs are provided, a GlueViz application window automatically launches with the various necessary plots. 
    Using GlueViz, users can perform various kinds of analyses on the data, like - selecting certain clusters on the 
    ordered-density plot of a particular feature space and visualize those clusters in other plots, i.e, all the plots are linked.
    
    Parameters
    ---------
    Note that all parameters of AstroGlue are optional. If passed and set using set_variables() method, the user would not see the
    tkinter GUI. If not passed, then the user will be prompted to input the parameters through the GUI.
    
    file_path : 'str'
            The absolute path to the .NPY or .CSV file containing galaxy data. Replace all single backslashes with double 
            backslashes.

    data_df : 'pandas dataframe'
            The data from the input .NPY or .CSV file converted to a pandas dataframe object with the column names specified.

    type_l : 'list'
            A list of the names of the type of plot that can be used in GlueViz. Currently the following plot types are supported:
            -> 1D Histogram
            -> 2D Scatter Plot (rectilinear)
            -> 2D Scatter Plot (aitoff)
            -> 3D Scatter Plot

    var_plot_list : 'list'
            A list of lists containing the column names to be plotted in GlueViz, corresponding to type_l. Each inner list must 
            contain between 1 and 3 column names. This means that for each plot specified by type_l, a minimum of 1 column name 
            and a maximum of 3 column names can be plotted.
    
    feature_space_name : 'list'
            A list of the names provided to a feature space over which Astrolink clustering algorithm would run and produce ordered
            density plots.

    feature_spaces : 'list'
            A list of lists containing the column names to be included in the feature space corresponding to 'feature_space_name'.
            Any number of column names can be included in a single feature space over which AstroLink clustering algorithm would
            run and produce ordered-density plots.

    adaptive_list : 'list'
            A list containing the adaptive parameter setting for feature space corresponding to 'feature_space_name'.

    k_den_list : 'list'
            A list containing the number of nearest neighbours parameter setting for feature space corresponding to 
            'feature_space_name'.

    S_list : 'list'
            A list containing the sensitivity threshold parameter setting for feature space corresponding to 'feature_space_name'.

    k_link_list : 'list'
            A list containing the number of nearest neighbours used to aggregate points parameter setting for feature space 
            corresponding to 'feature_space_name'

    h_style_list : 'list'
            A list containing the behaviour of the cluster hierarchy parameter setting for feature space 
            corresponding to 'feature_space_name'

    workers_list : 'list'
            A list containing the number of processors used in parallelised computations parameter setting for feature space 
            corresponding to 'feature_space_name'

    verbose_list : 'list'
            A list containing the verbosity parameter setting for feature space corresponding to 'feature_space_name'.
    """
    def __init__(self):
        self.file_path = None
        self.data_df = None
        self.feature_spaces = None
        self.adaptive_list = None
        self.k_den_list = None
        self.S_list = None
        self.k_link_list = None
        self.h_style_list = None
        self.workers_list = None
        self.verbose_list = None
        self.feature_space_name = None
        self.var_plot_list = None
        self.type_l = None
        self.groups_l = None

        self.P = None
        self.astrolink_list = []
        self.master_df = None
        self.dc = None
        self.ga = None
        self.col_l = [f"C{i}" for i in range(10) if i != 3]
        self.ord_ind_l = []
        self.log_rho_l = []

    #Function to accept variables directly without using the tkinter GUI
    def set_variables(self, file_path, data_df, feature_spaces, adaptive_list, k_den_list, S_list, k_link_list, h_style_list, workers_list, verbose_list, feature_space_name, var_plot_list, type_l):
        """This method of the AstroGlue can be used to set values to the variables used without having to input through the GUI.
        """
        self.file_path = file_path.replace("\\", "\\\\")
        self.data_df = data_df
        self.feature_spaces = feature_spaces
        self.adaptive_list = adaptive_list
        self.k_den_list = k_den_list
        self.S_list = S_list
        self.k_link_list = k_link_list
        self.h_style_list = h_style_list
        self.workers_list = workers_list
        self.verbose_list = verbose_list
        self.feature_space_name = feature_space_name
        self.var_plot_list = var_plot_list
        self.type_l = type_l

    def get_index(self, fi):
        return [self.data_df.columns.get_loc(col) for col in fi]
    
    def data_prep(self):
        indi_l = []
        for i in range(0, len(self.data_df.columns)):
            indi_l.append(list(self.P[:, i]))
        transposed_indi_l = list(zip(*indi_l))
        master_list = []
        for i in range(len(self.astrolink_list)):
            l1 = list(range(self.astrolink_list[i].n_samples))
            l2 = list(self.astrolink_list[i].logRho[self.astrolink_list[i].ordering])
            df1 = pd.DataFrame(list(zip(l1, l2)), columns=[self.ord_ind_l[i], self.log_rho_l[i]])

            df2 = pd.DataFrame(transposed_indi_l, columns=self.data_df.columns)
            df2[self.ord_ind_l[i]] = self.astrolink_list[i].ordering.argsort()

            try:
                merged_df1.drop()
            except:
                pass
            merged_df1 = pd.merge(df2, df1, on=self.ord_ind_l[i], sort=False)
            merged_df1["input order"] = merged_df1.index

            master_list.append(merged_df1)
        master_df = master_list[0]
        for i in range(1, len(master_list)):
            master_list[i] = master_list[i][["input order", self.ord_ind_l[i], self.log_rho_l[i]]]
            master_df = pd.merge(master_df, master_list[i], on='input order', how='inner')
        return master_df

    def make_ordered_density_plots(self, ax, c):
        """Makes the ordered density plots for the various feature spaces."""
        logRho_ordered = c.logRho[c.ordering]
        ax.plot(range(c.n_samples), logRho_ordered, 'k-', lw=0.1, zorder=2)
        ax.fill_between(range(c.n_samples), logRho_ordered, 0, color='k', label=c.ids[0], zorder=1)
        rootClstBool = np.ones(c.n_samples, dtype=np.bool_)
        for i, (clst, clst_id) in enumerate(zip(c.clusters, c.ids)):
            if i > 0:
                rootClstBool[clst[0]:clst[1]] = 0
                ord_dens_clst = logRho_ordered[clst[0]:clst[1]]
                colo = (i - 1) % 9
                ax.fill_between(range(clst[0], clst[1]), ord_dens_clst, ord_dens_clst.min(), color=self.col_l[colo], label=clst_id, zorder=1)
        ax.figure.canvas.draw()

    def plot_2d_scatter_rectilinear(self, x, y):
        """To plot 2D Rectilinear Scatter Plot"""
        scatter = self.ga.new_data_viewer(ScatterViewer)
        scatter.add_data(self.dc['dataframe'])
        scatter.state.x_att = self.dc['dataframe'].id[x]
        scatter.state.y_att = self.dc['dataframe'].id[y]
        scatter.state.size = 5

    def plot_2d_scatter_aitoff(self, x, y):
        """To plot 2D Aitoff Scatter Plot"""
        scatter = self.ga.new_data_viewer(ScatterViewer)
        scatter.add_data(self.dc['dataframe'])
        scatter.state.x_att = self.dc['dataframe'].id[x]
        scatter.state.y_att = self.dc['dataframe'].id[y]
        scatter.state.size = 5
        scatter.state.plot_mode = "aitoff"

    def plot_3d_scatter(self, x, y, z):
        """To plot 3D Scatter Plot"""
        scatter = self.ga.new_data_viewer(VispyScatterViewer)
        scatter.add_data(self.dc['dataframe'])
        scatter.state.x_att = self.dc['dataframe'].id[x]
        scatter.state.y_att = self.dc['dataframe'].id[y]
        scatter.state.z_att = self.dc['dataframe'].id[z]

    def plot_1d_histogram(self, x):
        """To plot 1D Histogram"""
        histo = self.ga.new_data_viewer(HistogramViewer)
        histo.add_data(self.dc["dataframe"])
        histo.state.x_att = self.dc['dataframe'].id[x]

    def run(self):
        """Runs AstroGlue. If inputs are provided usign set_variables() method, it directly opens Glueviz. If inputs are not
        provided then it launches the tkinter GUI window prompting user to input all the required fields."""
        if self.file_path is None or self.data_df is None or self.feature_spaces is None:
            self.tkinter_show()

        # Load the numpy file
        if self.file_path.endswith('.npy'):
            self.P = np.load(self.file_path)
        elif self.file_path.endswith('.csv'):
            self.P = self.data_df.to_numpy()

        # Run astrolink
        if len(self.feature_spaces) != 0:
            print("Running AstroLink...")
            for i in range(len(self.feature_spaces)):
                ind = self.get_index(self.feature_spaces[i])
                c = AstroLink(self.P[:, ind], adaptive=self.adaptive_list[i], k_den=self.k_den_list[i],
                              S=self.S_list[i], k_link=self.k_link_list[i], h_style=self.h_style_list[i],
                              workers=self.workers_list[i], verbose=self.verbose_list[i])
                self.astrolink_list.append(c)
                c.run()

        # Organizing lists
        for i in self.feature_space_name:
            self.ord_ind_l.append("ordered_index_" + i)
            self.log_rho_l.append("log_rho_" + i)

        # Prepare the data
        if len(self.astrolink_list) != 0:
            print("Preparing data")
            self.master_df = self.data_prep()
        else:
            self.master_df = self.data_df

        # Start Glueviz
        print("Starting Glueviz")
        self.dc = DataCollection()
        self.dc['dataframe'] = self.master_df
        self.ga = GlueApplication(self.dc)

        # Plot ordered density plots
        for i in range(len(self.astrolink_list)):
            scatter1 = self.ga.new_data_viewer(ScatterViewer)
            scatter1.add_data(self.dc['dataframe'])
            scatter1.state.x_att = self.dc['dataframe'].id[self.ord_ind_l[i]]
            scatter1.state.y_att = self.dc['dataframe'].id[self.log_rho_l[i]]
            viewer = self.ga.viewers[0][i]
            ax = viewer.axes
            ax.set_title("Ordered-Density Plot for " + self.feature_space_name[i] + " Space (coloured by cluster ID)")
            self.make_ordered_density_plots(ax, self.astrolink_list[i])

        # Plot other types of plots
        for i in range(len(self.var_plot_list)):
            if self.type_l[i] == "2D Scatter Plot (rectilinear)":
                x_ax = self.var_plot_list[i][0]
                y_ax = self.var_plot_list[i][1]
                self.plot_2d_scatter_rectilinear(x_ax, y_ax)
            elif self.type_l[i] == "3D Scatter Plot":
                x_ax = self.var_plot_list[i][0]
                y_ax = self.var_plot_list[i][1]
                z_ax = self.var_plot_list[i][2]
                self.plot_3d_scatter(x_ax, y_ax, z_ax)
            elif self.type_l[i] == "1D Histogram":
                x_ax = self.var_plot_list[i][0]
                self.plot_1d_histogram(x_ax)
            elif self.type_l[i] == "2D Scatter Plot (aitoff)":
                x_ax = self.var_plot_list[i][0]
                y_ax = self.var_plot_list[i][1]
                self.plot_2d_scatter_aitoff(x_ax, y_ax)

        # Arrange in a grid
        self.ga.gather_current_tab()

        # Start the application
        self.ga.start(maximized=True)

    def tkinter_show(self):
        global data_df,f2_row,f3_row,type_l,dropdown_l,feature_spaces,feature_space_name,adaptive_list,k_den_list,S_list,k_link_list,h_style_list,workers_list,verbose_list,groups_l
        data_df = 0
        f2_row = -1
        f3_row = -1
        type_l = []
        dropdown_l = []
        feature_spaces = []
        feature_space_name = []
        adaptive_list = []
        k_den_list = []
        S_list = []
        k_link_list = []
        h_style_list = []
        workers_list = []
        verbose_list = []
        groups_l={}

        def get_groups():
            col_l = data_df.columns
            pattern1 = r'^v.*[xyz]$'
            pattern3 = r'^(?=.*[xyz])(?=.*kpc).*$|^[xyz]$'
            regex1 = re.compile(pattern1)
            regex2 = re.compile(pattern3)
            for i in col_l:
                if regex1.match(i):
                    try:
                        groups_l["Velocity"].append(i)
                    except:
                        groups_l["Velocity"]=[]
                        groups_l["Velocity"].append(i)
                elif regex2.match(i):
                    try:
                        groups_l["Position"].append(i)
                    except:
                        groups_l["Position"]=[]
                        groups_l["Position"].append(i)

        def upload_file():
            global file_path
            for widget in col_entry_inner_frame2.winfo_children():
                widget.destroy()
            for widget in col_entry_inner_frame3.winfo_children():
                widget.destroy()
            file_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy"), ("CSV files", "*.csv")])
            if file_path:
                basename = os.path.basename(file_path)
                file_label.config(text=basename)
                process_file(file_path)

        def process_file(file_path):
            global data_df
            if file_path.endswith('.npy'):
                data = np.load(file_path)
                data_df = pd.DataFrame(data, columns=[f"col{i+1}" for i in range(data.shape[1])])
            elif file_path.endswith('.csv'):
                data_df = pd.read_csv(file_path)
            root.after(0, update_ui, data_df)

        def update_ui(df):
            display_table(df)
            display_column_entries(df)

        def display_table(df):
            for item in tree.get_children():
                tree.delete(item)

            tree["columns"] = list(df.columns)
            tree["show"] = "headings"

            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='center') 

            max_rows = 50
            for i, row in df.iterrows():
                if i >= max_rows:
                    break
                tree.insert("", "end", values=list(row), tags=('oddrow' if i % 2 else 'evenrow',))

            tree.tag_configure('oddrow', background='lightgrey')
            tree.tag_configure('evenrow', background='white')

        def display_column_entries(df):
            for widget in col_entry_inner_frame.winfo_children():
                widget.destroy()

            columns = df.columns
            entries = []

            for i, col in enumerate(columns):
                label = Label(col_entry_inner_frame, text=col)
                label.grid(row=i, column=0, padx=5, pady=2)
                entry = Entry(col_entry_inner_frame)
                if file_path.endswith('.csv'):
                    entry.insert(0,col)
                entry.grid(row=i, column=1, padx=5, pady=2)
                
                entry.bind("<KeyRelease>", lambda event, entries=entries: check_entries(entries))
                entries.append(entry)

            update_button = Button(col_entry_inner_frame, text="Save and Next", command=lambda: update_columns(entries, df),cursor="hand2")
            update_button.grid(row=len(columns), column=0, columnspan=2, pady=10)
            if not file_path.endswith('.csv'):
                update_button.grid_remove()  

            def check_entries(entries):
                all_filled = all(entry.get() for entry in entries)
                if all_filled:
                    update_button.grid()  
                else:
                    update_button.grid_remove()  

        def update_columns(entries, df,f3_row=f3_row):
            new_columns = [entry.get() for entry in entries]
            df.columns = new_columns
            for widget in col_entry_inner_frame2.winfo_children():
                widget.destroy()
            for widget in col_entry_inner_frame3.winfo_children():
                widget.destroy()
            var = IntVar()
            f3_row+=1
            c1 = Checkbutton(col_entry_inner_frame3, text="Run AstroLink", variable=var, command=lambda: show_feature_space(f3_row))
            c1.grid(row=f3_row, column=0)
            get_groups()
            display_table(df)
            plot_options(f2_row)

        def selected(event, f2_row, clicked):
            s = clicked.get()
            if s == "2D Scatter Plot (rectilinear)":
                #type_l.append()
                create_dropdowns(2, f2_row,"2D Scatter Plot (rectilinear)")
            elif s == "3D Scatter Plot":
                #type_l.append("3D Scatter Plot")
                create_dropdowns(3, f2_row,"3D Scatter Plot")
            elif s=="1D Histogram":
                #type_l.append("1D Histogram")
                create_dropdowns(1,f2_row,"1D Histogram")
            elif s=="2D Scatter Plot (aitoff)":
                #type_l.append("2D Scatter Plot (aitoff)")
                create_dropdowns(2,f2_row,"2D Scatter Plot (aitoff)")

        def select_all(listbox):
            listbox.select_set(0,END)

        def select_var(b,listbox):
            button_list = groups_l[b]
            button_list_ind = []
            for i in button_list:
                button_list_ind.append(list(data_df.columns).index(i))
            for j in button_list_ind:
                listbox.select_set(j)   

        def remove_feature_space(f3_row):
            global feature_spaces, feature_space_name, adaptive_list, k_den_list, S_list, k_link_list, h_style_list, workers_list, verbose_list

            if feature_spaces:
                feature_spaces.pop()
                destroy_button2(row=f3_row, column=0)
                destroy_button2(row=f3_row, column=1)
                destroy_button2(row=f3_row-1, column=0)
                destroy_button2(row=f3_row-1, column=1)

                if f3_row >= 0:
                    feature_space_name.pop()
                    adaptive_list.pop()
                    k_den_list.pop()
                    S_list.pop()
                    k_link_list.pop()
                    h_style_list.pop()
                    workers_list.pop()
                    verbose_list.pop()
                
                f3_row -= 1

            create_button = Button(col_entry_inner_frame3, text="Create a new featurespace", command=lambda: show_feature_space(f3_row),cursor="hand2")
            create_button.grid(row=f3_row, column=0, pady=5, padx=5)
            
            if f3_row!=0:
                remove_feature_space_button = Button(col_entry_inner_frame3, text="Remove Feature Space", command=lambda: remove_feature_space(f3_row),cursor="hand2")
                remove_feature_space_button.grid(row=f3_row, column=1, pady=5)

        def on_destroy(f3_row):
            try:
                k=feature_space_name[f3_row-1]
            except:
                destroy_button2(row=f3_row, column=0)
                destroy_button2(row=f3_row, column=1)
                destroy_button2(row=f3_row-1, column=0)
                destroy_button2(row=f3_row-1, column=1)
                f3_row-=1
                create_button = Button(col_entry_inner_frame3, text="Create a new featurespace", command=lambda: show_feature_space(f3_row),cursor="hand2")
                create_button.grid(row=f3_row, column=0, pady=5, padx=5)
                
                if f3_row!=0:
                    remove_feature_space_button = Button(col_entry_inner_frame3, text="Remove Feature Space", command=lambda: remove_feature_space(f3_row),cursor="hand2")
                    remove_feature_space_button.grid(row=f3_row, column=1, pady=5)


        def show_feature_space(f3_row):
            global feature_spaces, f3_row_counter
            destroy_button2(f3_row, 0)
            destroy_button2(f3_row, 1)
            l1_3 = Label(col_entry_inner_frame3, text="Feature Space " + str(f3_row) + ":")
            l1_3.grid(row=f3_row, column=0, pady=5, padx=5)

            f3_row+=1
            create_button = Button(col_entry_inner_frame3, text="Create a new featurespace", command=lambda: show_feature_space(f3_row),cursor="hand2")
            create_button.grid(row=f3_row, column=0, pady=5, padx=5)
            
            remove_feature_space_button = Button(col_entry_inner_frame3, text="Remove Feature Space", command=lambda: remove_feature_space(f3_row),cursor="hand2")
            remove_feature_space_button.grid(row=f3_row, column=1, pady=5)

            root2 = tk.Tk()
            root2.bind("<Destroy>",lambda event,f3_row=f3_row:on_destroy(f3_row))
            root2.title("Choose features in this space")
            global curr_row
            curr_row = 0
            listbox = Listbox(root2, selectmode="multiple", exportselection=0)
            for col in data_df.columns:
                listbox.insert(END, col)
            if len(groups_l) > 0:
                listbox.grid(row=curr_row, column=0, pady=5, padx=5, rowspan=len(groups_l) + 1)
                Button(root2, text='Select All', command=lambda: select_all(listbox),cursor="hand2").grid(row=curr_row, column=1, padx=5, pady=2)
                if "Position" in groups_l.keys() and len(groups_l["Position"])>0:
                    curr_row += 1
                    Button(root2, text="Select Position", command=lambda: select_var("Position", listbox),cursor="hand2").grid(row=curr_row, column=1, padx=5, pady=2)
                if "Velocity" in groups_l.keys() and len(groups_l["Velocity"])>0:
                    curr_row += 1
                    Button(root2, text="Select Velocity", command=lambda: select_var("Velocity", listbox),cursor="hand2").grid(row=curr_row, column=1, padx=5, pady=2)
            else:
                listbox.grid(row=curr_row, column=0, pady=5, padx=5, rowspan=1)
                Button(root2, text='Select All', command=lambda: select_all(listbox),cursor="hand2").grid(row=curr_row, column=1, padx=5, pady=5)
            
            curr_row = len(groups_l) + 3

            root2_l1 = Label(root2, text="Enter a name for this feature space")
            root2_l1.grid(row=curr_row, column=0, pady=5, padx=5)
            
            root2_e1 = Entry(root2)
            root2_e1.grid(row=curr_row, column=1, pady=5, padx=5)
            curr_row += 1
            
            root2_l2 = Label(root2, text="Set adaptive: ")
            root2_l2.grid(row=curr_row, column=0, pady=5, padx=5)
            
            root2_e2 = Entry(root2)
            root2_e2.insert(0, "1")
            root2_e2.grid(row=curr_row, column=1, pady=5, padx=5)
            curr_row += 1

            modify_params_button = Button(root2, text="Modify other parameters", command=lambda: toggle_parameters(root2, curr_row),cursor="hand2")
            modify_params_button.grid(row=curr_row, columnspan=2, pady=5)
            global param_widgets
            param_widgets = []
            default_params = {"k_den": 20, "S": "auto", "k_link": "auto", "h_Style": 1, "workers": -1, "verbose": 0}

            for i in default_params:
                label = Label(root2, text=f"{i}")
                entry = Entry(root2)
                entry.insert(0, str(default_params[i]))
                param_widgets.append((label, entry))
            global hyperlink
            hyperlink = Label(root2, text="Go to docs", fg="blue", cursor="hand2")
            hyperlink.bind("<Button-1>", lambda e: webbrowser.open_new("https://astrolink.readthedocs.io/en/latest/api.html"))

            add_button = Button(root2, text="Add to Feature Space", command=lambda: add_to_feature_space(listbox, f3_row, root2, root2_e1, root2_e2),cursor="hand2")
            add_button.grid(row=curr_row + 5 + len(default_params), column=0, columnspan=2, pady=5)

        def toggle_parameters(root2,curr_row):
            curr_row+=1
            for widget_pair in param_widgets:
                widget_pair[0].grid(row=curr_row, column=0, pady=2, padx=5)
                widget_pair[1].grid(row=curr_row, column=1, pady=2, padx=5)
                curr_row+=1
            hyperlink.grid(row=14, column=0, columnspan=2, pady=5)

        def add_to_feature_space(listbox, f3_row,root2,root2_e1,root2_e2):
            global feature_spaces
            group_label = root2_e1.get()
            feature_space_name.append(group_label)
            adaptive_val = root2_e2.get()
            adaptive_list.append(int(root2_e2.get()))
            selected_indices = listbox.curselection()
            selected_columns = [listbox.get(i) for i in selected_indices]
            for count_j in range(len(param_widgets)):
                widget_pair = param_widgets[count_j]
                if count_j==0:
                    k_den_list.append(int(widget_pair[1].get()))
                elif count_j==1:
                    try:
                        S_list.append(float(widget_pair[1].get()))
                    except:
                        S_list.append(str(widget_pair[1].get()))
                elif count_j==2:
                    try:
                        k_link_list.append(int(widget_pair[1].get()))
                    except:
                        k_link_list.append(str(widget_pair[1].get()))
                elif count_j==3:
                    h_style_list.append(int(widget_pair[1].get()))
                elif count_j==4:
                    workers_list.append(int(widget_pair[1].get()))
                elif count_j==5:
                    verbose_list.append(int(widget_pair[1].get()))
            root2.destroy()
            l3_1 = Label(col_entry_inner_frame3,text="You have selected: "+str(selected_columns)+" - "+str(group_label))
            l3_1.grid(row=f3_row-1,column=1)
            feature_spaces.append(selected_columns)

        def destroy_button2(row, column):
            for widget in col_entry_inner_frame3.grid_slaves(row=row, column=column):
                widget.destroy()

        def pull_featurespace(f3_row):
            f3_row+=1
            b1_3 = Button(col_entry_inner_frame3, text="Create a new featurespace", command=lambda: show_feature_space(f3_row),cursor="hand2")
            b1_3.grid(row=f3_row, column=0, pady=5)

        def del_prev_plot(f2_row):
            for widget in col_entry_inner_frame2.grid_slaves(row=f2_row):
                widget.destroy()
            f2_row-=1
            for widget in col_entry_inner_frame2.grid_slaves(row=f2_row):
                widget.destroy()
            dropdown_l.pop(f2_row)
            type_l.pop(f2_row)
            b1 = Button(col_entry_inner_frame2, text="Create a new plot", command=lambda: show_plot_options(f2_row),cursor="hand2")
            b1.grid(row=f2_row, column=0, pady=5)

            if f2_row!=0:
                b2 = Button(col_entry_inner_frame2, text="Delete Previous Plot", command=lambda: del_prev_plot(f2_row),cursor="hand2")
                b2.grid(row=f2_row, column=1, pady=5)

        def create_dropdowns(num_dropdowns, f2_row,name):
            dropdowns = []
            options = data_df.columns
            try:
                for widget in col_entry_inner_frame2.grid_slaves(row=f2_row, column=1):
                    dropdown_l.pop(f2_row)
                    type_l.pop(f2_row)
                    widget.destroy()
            except:
                pass
            try:        
                for widget in col_entry_inner_frame2.grid_slaves(row=f2_row, column=2):
                    widget.destroy()
            except:
                pass
            try:        
                for widget in col_entry_inner_frame2.grid_slaves(row=f2_row, column=3):
                    widget.destroy()
            except:
                pass
                    
            for i in range(num_dropdowns):
                clicked = StringVar()
                clicked.set(options[0])
                dropdown = OptionMenu(col_entry_inner_frame2, clicked, *options)
                dropdown.grid(row=f2_row, column=i+1, pady=5, padx=5)
                dropdowns.append(clicked)
            f2_row += 1
            dropdown_l.append(dropdowns)
            type_l.append(name)
            b1 = Button(col_entry_inner_frame2, text="Create a new plot", command=lambda: show_plot_options(f2_row),cursor="hand2")
            b1.grid(row=f2_row, column=0, pady=5)

            if f2_row!=0:
                b2 = Button(col_entry_inner_frame2, text="Delete Previous Plot", command=lambda: del_prev_plot(f2_row),cursor="hand2")
                b2.grid(row=f2_row, column=1, pady=5)

        def show_plot_options(f2_row):
            clicked = StringVar()
            options = ["Select a Plot", "1D Histogram", "2D Scatter Plot (rectilinear)","2D Scatter Plot (aitoff)", "3D Scatter Plot"]
            clicked.set(options[0])
            drop1 = OptionMenu(col_entry_inner_frame2, clicked, *options, command=lambda event: selected(event, f2_row, clicked))
            destroy_button(f2_row, 0)
            try:
                destroy_button(f2_row, 1)
            except:
                pass
            drop1.grid(row=f2_row, column=0, pady=5)

        def destroy_button(row, column):
            for widget in col_entry_inner_frame2.grid_slaves(row=row, column=column):
                widget.destroy()
            

        def plot_options(f2_row):
            f2_row += 1
            b1 = Button(col_entry_inner_frame2, text="Create a new plot", command=lambda: show_plot_options(f2_row),cursor="hand2")
            b1.grid(row=f2_row, column=0, pady=5)

        root = tk.Tk()
        root.title("AstroGlue")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        title_label = Label(root,text="AstroGlue",font=("Arial", 25))
        title_label.pack(padx=5)

        file_prompt_frame = LabelFrame(root, text="Upload Data File")
        file_prompt_frame.pack(fill="x", padx=10, pady=5)

        upload_button = tk.Button(file_prompt_frame, text="Upload File", command=upload_file,cursor="hand2")
        upload_button.pack(padx=10, pady=5)

        file_label = tk.Label(file_prompt_frame, text="")
        file_label.pack(padx=10, pady=5)

        table_frame = LabelFrame(root, text="Data Table")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tree = ttk.Treeview(table_frame)
        tree.pack(side="left", fill="both", expand=True)

        table_scrollbar_y = Scrollbar(table_frame, orient="vertical", command=tree.yview)
        table_scrollbar_x = Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=table_scrollbar_y.set, xscroll=table_scrollbar_x.set)
        table_scrollbar_y.pack(side="right", fill="y")
        table_scrollbar_x.pack(side="bottom", fill="x")

        main_frame = Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        f1 = LabelFrame(main_frame, text="Column Names")
        f1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        col_entry_canvas = Canvas(f1)
        col_entry_scrollbar_y = Scrollbar(f1, orient="vertical", command=col_entry_canvas.yview)
        col_entry_scrollbar_x = Scrollbar(f1, orient="horizontal", command=col_entry_canvas.xview)
        col_entry_inner_frame = Frame(col_entry_canvas)

        col_entry_inner_frame.bind(
        "<Configure>",
        lambda e: col_entry_canvas.configure(
            scrollregion=col_entry_canvas.bbox("all")
        )
        )

        col_entry_canvas.create_window((0, 0), window=col_entry_inner_frame, anchor="nw")

        col_entry_canvas.configure(yscrollcommand=col_entry_scrollbar_y.set, xscrollcommand=col_entry_scrollbar_x.set)
        col_entry_canvas.pack(side="left", fill="both", expand=True)
        col_entry_scrollbar_y.pack(side="right", fill="y")
        col_entry_scrollbar_x.pack(side="bottom", fill="x")

        f2 = LabelFrame(main_frame, text="Choose Plots")
        f2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        col_entry_canvas2 = Canvas(f2)
        col_entry_scrollbar_y2 = Scrollbar(f2, orient="vertical", command=col_entry_canvas2.yview)
        col_entry_scrollbar_x2 = Scrollbar(f2, orient="horizontal", command=col_entry_canvas2.xview)
        col_entry_inner_frame2 = Frame(col_entry_canvas2)

        col_entry_inner_frame2.bind(
        "<Configure>",
        lambda e: col_entry_canvas2.configure(
            scrollregion=col_entry_canvas2.bbox("all")
        )
        )

        col_entry_canvas2.create_window((0, 0), window=col_entry_inner_frame2, anchor="nw")
        col_entry_canvas2.configure(yscrollcommand=col_entry_scrollbar_y2.set, xscrollcommand=col_entry_scrollbar_x2.set)
        col_entry_canvas2.pack(side="left", fill="both", expand=True)
        col_entry_scrollbar_y2.pack(side="right", fill="y")
        col_entry_scrollbar_x2.pack(side="bottom", fill="x")

        f3 = LabelFrame(main_frame, text="AstroLink Frame")
        f3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        col_entry_canvas3 = Canvas(f3)
        col_entry_scrollbar_y3 = Scrollbar(f3, orient="vertical", command=col_entry_canvas3.yview)
        col_entry_scrollbar_x3 = Scrollbar(f3, orient="horizontal", command=col_entry_canvas3.xview)
        col_entry_inner_frame3 = Frame(col_entry_canvas3)

        col_entry_inner_frame3.bind(
        "<Configure>",
        lambda e: col_entry_canvas3.configure(
            scrollregion=col_entry_canvas3.bbox("all")
        )
        )

        col_entry_canvas3.create_window((0, 0), window=col_entry_inner_frame3, anchor="nw")

        col_entry_canvas3.configure(yscrollcommand=col_entry_scrollbar_y3.set, xscrollcommand=col_entry_scrollbar_x3.set)
        col_entry_canvas3.pack(side="left", fill="both", expand=True)
        col_entry_scrollbar_y3.pack(side="right", fill="y")
        col_entry_scrollbar_x3.pack(side="bottom", fill="x")

        main_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        main_frame.grid_columnconfigure(1, weight=3, uniform="group1")
        main_frame.grid_columnconfigure(2, weight=2, uniform="group1")

        def close_win():
            root.destroy()
            len_plot_list = []
            var_plot_list =[]
            for i in dropdown_l:
                len_plot_list.append(len(i))
                l1_list =[]
                for j in i:
                    s = j.get()
                    l1_list.append(s)
                var_plot_list.append(l1_list)

            #Reassigning all variables
            self.data_df = data_df
            self.type_l = type_l
            self.feature_spaces = feature_spaces
            self.feature_space_name = feature_space_name
            self.adaptive_list =adaptive_list
            self.k_den_list = k_den_list
            self.S_list = S_list
            self.k_link_list = k_link_list
            self.h_style_list = h_style_list
            self.workers_list = workers_list
            self.verbose_list = verbose_list
            self.groups_l = groups_l
            self.var_plot_list = var_plot_list
            self.file_path = file_path

        end_button = Button(root,text="Save Preferences and Start -->",command = close_win,cursor="hand2",font=("Arial", 10))
        end_button.pack(padx=5,pady=1)

        root.mainloop()