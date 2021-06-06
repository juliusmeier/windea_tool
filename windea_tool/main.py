import pkg_resources
import os
import pandas as pd
import numpy as np
from windea_tool import weibull
from windea_tool import plotting
import copy

turbines_dict = {'Enercon E-33 (330 kW)':'Enercon_E-33_330kW.xlsx',
                 'Enercon E-30 (200 kW)':'Enercon_E-30_200kW.xlsx',
                 'Enercon E-115 (3000 kW)':'Enercon_E-115_3000kW.xlsx'}

class Windea:

    def __init__(self, start=0, stop=30, step=1):
        self.turbines_container = {}
        self.locations_container = {}
        self.analysis_container = {}
        #v = np.arange(start, stop + step, step)
        #self.v = v
        #self.df_main = pd.DataFrame(index=v)


    def add_turbine(self, turbine_name):
        new_turbine = Turbine(turbine_name)
        self.turbines_container[turbine_name] = new_turbine

    def add_location(self, location_name, A=None, k=None, v_m=None): # weibull oder messung, windprofil
        new_location = Location(location_name, A=A, k=k, v_m=v_m)
        self.locations_container[location_name] = new_location

    def analyse(self, name, loc=None, turb=None): #wenn keine turb, loc auswahl getroffen, nimm alles aus containern, sonst nimm auswahl.
        # if isinstance(loc, list) and isinstance(turbs, list):
        #    raise Exception
        if loc is None and turb is None:
            print("Analyse aller geladenen Turbinen und Standorte")
            if len(self.locations_container) > 1 and len(self.turbines_container) > 1:
                print("Mehrere Turbinen und mehrere Standorte. Bitte Auswahl treffen")
                #raise Exception
            # STOP!!!
            new_analysis = Analysis(name)
            new_analysis.locations = copy.copy(self.locations_container)
            new_analysis.turbines = copy.copy(self.turbines_container)
            self.analysis_container[name] = new_analysis
            new_analysis.ertrag()
            # falls loc und turb mehrere, abfangen!

        # 3 Fälle unterscheiden:
        if isinstance(loc, str) and isinstance(turb, str):
            print("Analyse einer Windturbine an einem Standort")
            new_analysis = Analysis(name)
            new_analysis.locations[loc] = copy.copy(self.locations_container[loc])
            new_analysis.turbines[turb] = copy.copy(self.turbines_container[turb])
            self.analysis_container[name] = new_analysis
            new_analysis.ertrag()
        if isinstance(loc, str) and isinstance(turb, list):
            print("Analyse verschiedener Windturbinen für einen Standort")
            new_analysis = Analysis(name)
            new_analysis.locations[loc] = copy.copy(self.locations_container[loc])
            for t in turb:
                new_analysis.turbines[t] = copy.copy(self.turbines_container[t])
            self.analysis_container[name] = new_analysis
            new_analysis.ertrag()
        if isinstance(loc, list) and isinstance(turb, str):
            print("Analyse einer Windturbine an verschiedenen Standorten")
            new_analysis = Analysis(name)
            for l in loc:
                new_analysis.locations[l] = copy.copy(self.locations_container[l])
            new_analysis.turbines[turb] = copy.copy(self.turbines_container[turb])
            self.analysis_container[name] = new_analysis
            new_analysis.ertrag()


    def windhistogramm(self, A=None, k=None, v_m=None):
        self.df_weibull, self.df_weibull_detailed = weibull.weibull_windhistogramm(A=A, k=k, v_m=v_m)
        # weibull oder messung

    def plot(self, analysis, selected_plots=["windhistogramm", "turbine", "main", "ertrag", "ertrag_h"]):
        A = self.analysis_container[analysis]
        fig_list = []

        if "windhistogramm" in selected_plots:
            fig_list.append(plotting.plot_weibull(A.locations))
        if "turbine" in selected_plots:
            fig_list.append(plotting.plot_turbine(A.turbines))
        if "main" in selected_plots:
            for turb in A.turbines.values():
                fig_list.append(plotting.plot_main(turb))
            #for loc in A.locations.values():
            #    fig_list.append(plotting.plot_main(loc))
        if "ertrag" in selected_plots:
            fig_list.append(plotting.plot_ertrag(A.turbines))
        if "ertrag_h" in selected_plots:
            fig_list.append(plotting.plot_ertrag_h(A.turbines))


    def save_plots(self, path=""):
        plots_dir = path + "plots/"
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
        for fig in self.fig_list:
            fig.savefig(plots_dir + fig.texts[0].get_text() + ".png")
            #fig.savefig(plots_dir + fig.texts[0].get_text() + ".pdf")

    def save_data(self, analysis, path=""):
        A = self.analysis_container[analysis]
        print(A.turbines)
        print(A.locations)

        #w = [i for i in self.locations_container.values()]
        Excelwriter = pd.ExcelWriter(A.name+".xlsx", engine="xlsxwriter")
        #for i in w:
        A.pp_data.to_excel(Excelwriter, sheet_name=A.name, index=False)
        Excelwriter.save()


    def postprocessing_1(self, analysis):
        A = self.analysis_container[analysis]

        A.pp_data=pd.DataFrame()

        df_list = []
        loc_obj = list(A.locations.values())[0]

        df_list.append(loc_obj.df_weibull)
        for turb in loc_obj.turbines:
            a = pd.DataFrame({turb:[]})
            df_list.append(a)
            df_list.append(A.turbines[turb].df_main)
        A.pp_data = pd.concat(df_list, axis=1)

    def postprocessing_2(self, analysis):
        A = self.analysis_container[analysis]

        A.pp_data=pd.DataFrame()

        df_list = []
        turb_obj = list(A.turbines.values())[0]

        df_list.append(turb_obj.df_turbine)
        for loc in turb_obj.locations:
            print(loc)
            a = pd.DataFrame({loc:[]})
            df_list.append(a)
            df_list.append(A.locations[loc].df_main)
        A.pp_data = pd.concat(df_list, axis=1)

class Turbine:

    def __init__(self, turbine_name):
        self.turbine_name = turbine_name
        self.df_turbine = load_turbine(turbine_name)
        #self.df_main = pd.DataFrame()
        self.locations = []

class Location:

    def __init__(self, name, A=None, k=None, v_m=None):
        self.name = name
        self.A = A
        self.k = k
        self.v_m = v_m
        self.df_weibull, self.df_weibull_detailed = weibull.weibull_windhistogramm(A=A, k=k, v_m=v_m)
        self.turbines = []

class Analysis:

    def __init__(self, name):
        self.name = name
        self.turbines = {}
        self.locations = {}
        #self.df_main = {}

    def ertrag(self):
        if len(self.locations) == 1:
            for turb, obj in self.turbines.items():
                # get location_name and location_object of the single location in loc_dict of Analysis object
                loc = list(self.locations.keys())[0]
                loc_obj = list(self.locations.values())[0]
                # document location_name in turbine object and turbine_name in location object
                obj.locations.append(loc)
                loc_obj.turbines.append(obj.turbine_name)
                # initialize df_main of Analysis object
                df_main = pd.DataFrame()
                df_main['v'] = obj.df_turbine['v']
                df_main['h'] = loc_obj.df_weibull['h']
                df_main['P'] = obj.df_turbine['P']
                # perform calculations of energy yield
                df_main['E'] = df_main['h'] * df_main['P'] * 8760 / 1000 ** 2  # GWh
                df_main['E_h'] = df_main['E'] / df_main['E'].sum()
                obj.df_main = df_main
        elif len(self.locations) > 1:
            print("Mehrere Locations")
            for loc, obj in self.locations.items():
                # get turbine_name and turbine_object of the single turbine in turbine_dict of Analysis object
                turb = list(self.turbines.keys())[0]
                turb_obj = list(self.turbines.values())[0]
                # document location_name in turbine object and turbine_name in location object
                obj.turbines.append(turb)
                turb_obj.locations.append(loc)
                # initialize df_main of Analysis object
                df_main = pd.DataFrame()
                df_main['v'] = turb_obj.df_turbine['v']
                df_main['h'] = obj.df_weibull['h']
                df_main['P'] = turb_obj.df_turbine['P']
                # perform calculations of energy yield
                df_main['E'] = df_main['h'] * df_main['P'] * 8760 / 1000 ** 2  # GWh
                df_main['E_h'] = df_main['E'] / df_main['E'].sum()
                obj.df_main = df_main
                #print(df_main)


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