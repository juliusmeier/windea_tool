import pkg_resources
import os
import pandas as pd
import numpy as np
from windea_tool import weibull
from windea_tool import plotting

turbines_dict = {'Enercon E-33 (330 kW)':'Enercon_E-33_330kW.xlsx',
                 'Enercon E-30 (200 kW)':'Enercon_E-30_200kW.xlsx',
                 'Enercon E-115 (3000 kW)':'Enercon_E-115_3000kW.xlsx'}

class Windea:

    def __init__(self, start=0, stop=30, step=1):
        self.turbines_container = []
        self.locations_container = []
        v = np.arange(start, stop + step, step)
        self.v = v
        #self.df_main = pd.DataFrame(index=v)


    def analyse(self, turbine, A=None, k=None, v_m=None):
        print("analyse")

    def add_turbine(self, turbine_name):
        new_turbine = Turbine(turbine_name)
        self.turbines_container.append(new_turbine)

        #df_container = []
        #df_turbine = load_turbine(turbine).copy()
        #self.turbines_container[turbine] = df_container
        #self.turbines_container[turbine].append(df_turbine)

        #print(self.turbines_dict)
        #print(self.turbines_dict[turbine])
        #self.turbines = []
        #self.turbines.append(load_turbine(turbine))

    def add_location(self, name, A=None, k=None, v_m=None):
        new_location = Location(name, A=A, k=k, v_m=v_m)
        self.locations_container.append(new_location)

    def windhistogramm(self, A=None, k=None, v_m=None):
        self.df_weibull, self.df_weibull_detailed = weibull.weibull_windhistogramm(A=A, k=k, v_m=v_m)
        # weibull oder messung

    def t(self):
        for turb in self.turbines_container:
            self.ertrag(turb, self.locations_container[0])

    def ertrag(self, turbine, location):
        turbine.locations = location.name
        location.turbines = turbine.turbine_name
        turbine.df_main = turbine.df_turbine
        turbine.df_main['h'] = location.df_weibull['h']

        turbine.df_main['E'] = turbine.df_main['h'] * turbine.df_main['P'] * 8760 / 1000 ** 2  # GWh
        turbine.df_main['E_h'] = turbine.df_main['E'] / turbine.df_main['E'].sum()


    def plot_all(self):
        fig_list = []
        for loc in self.locations_container:
            fig_list.append(plotting.plot_weibull(loc))
        fig_list.append(plotting.plot_turbine(self.turbines_container))
        for turb in self.turbines_container:
            fig_list.append(plotting.plot_main(turb))
        fig_list.append(plotting.plot_ertrag(self.turbines_container, ylabel="Windenergieertrag in GWh",
                                             title="Ertragsverteilung in GWh", color="blue"))
        fig_list.append(plotting.plot_ertrag_h(self.turbines_container))
        self.fig_list = fig_list

    def save_plots(self, path=""):
        plots_dir = path + "plots/"
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
        for fig in self.fig_list:
            fig.savefig(plots_dir + fig.texts[0].get_text() + ".png")
            #fig.savefig(plots_dir + fig.texts[0].get_text() + ".pdf")

    def save_data(self, path=""):
        #data_dir = path + "data/"
        #if not os.path.exists(data_dir):
        #    os.makedirs(data_dir)

        df_list = self.turbines_container
        # We'll define an Excel writer object and the target file
        Excelwriter = pd.ExcelWriter("data.xlsx", engine="xlsxwriter")
        # We now loop process the list of dataframes
        for df in df_list:
            df.df_main.to_excel(Excelwriter, sheet_name=df.turbine_name, index=False)
        # And finally save the file
        Excelwriter.save()

    def postprocessing(self):
        print('postprocessing')


class Turbine:

    def __init__(self, turbine_name):
        self.turbine_name = turbine_name
        self.df_turbine = load_turbine(turbine_name)
        self.df_main = pd.DataFrame()

class Location:

    def __init__(self, name, A=None, k=None, v_m=None):
        self.name = name
        self.A = A
        self.k = k
        self.v_m = v_m
        self.df_weibull, self.df_weibull_detailed = weibull.weibull_windhistogramm(A=A, k=k, v_m=v_m)
        self.turbines = []


def load_turbine(turbine):
    path = "data/" + turbines_dict[turbine]
    data = pkg_resources.resource_string(__name__, path)
    return pd.read_excel(data, engine = 'openpyxl', header=1)


def save_plots(fig_list, path=""):
    plots_dir = path+"plots/"
    os.makedirs(plots_dir)
    for fig in fig_list:
        fig.savefig(plots_dir + fig.texts[0].get_text() + ".png")
        #fig.savefig(plots_dir + fig.texts[0].get_text() + ".pdf")

def save_data(df, path=""):
    data_dir = path + "data/"
    os.makedirs(data_dir)
    df.to_excel(data_dir + "data.xlsx", index=False)

def save_all():
    print('save all')
    #save_plots(path, fig_list)
    #save_data(path)

def report():
    print('report with pandoc? Shell-command')


"""
def ertrag(df, en):
    df['P'] = en['P'] # kW
    df['E'] = df['h'] * df['P'] * 8760 / 1000**2 # GWh
    df['E_h'] = df['E'] / df['E'].sum()
    df['h'] = df['h']
"""