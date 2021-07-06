import pkg_resources
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windea_tool import weibull
from windea_tool import plotting

turbines_dict = {'Enercon E-70 (2300 kW)':'Enercon_E-70_2300kW.xlsx',
                 'Enercon E-115 (3000 kW)':'Enercon_E-115_3000kW.xlsx'}

class Windea:

    def __init__(self, name, start=0, stop=30, step=1):
        self.turbines_container = {}
        self.locations_container = {}
        self.analysis_container = {}
        self.name = name
        self.df_main = {}
        #v = np.arange(start, stop + step, step)
        #self.v = v
        #self.df_main = pd.DataFrame(index=v)


    def add_turbine(self, name, rho = 1.225, verfügbarkeit = 1, path=""):
        new_turbine = Turbine(name=name, rho=rho, verfügbarkeit=verfügbarkeit, path=path)
        self.turbines_container[name] = new_turbine

    def add_location(self, name, delta_v = 1, A=None, k=None, v_m=None, h = None,
                     start = 0, stop = 160, step = 10, type_windprofil = None, v_r = None, h_r = None,
                     z_0 = None, a = None,
                     type=None, path=""):
        new_location = Location(name, delta_v = delta_v, A=A, k=k, v_m=v_m, type=type, path=path)
        self.locations_container[name] = new_location
        # override Location with wind data in reference height with data in hub height
        if type_windprofil is not None:
            self.add_windprofil(location=name, start=start, stop=stop, step=step,
                                type=type_windprofil, v_r=v_r, h_r=h_r, z_0=z_0, a=a)
            v_h = self.get_v_in_h(name, h=h)

            new_location = Location(name, delta_v = delta_v, A=A, k=k, v_m=v_h, type=type, path=path)
            self.locations_container[name] = new_location

    def add_windprofil(self, location, start, stop, step, type, v_r, h_r, z_0 = None, a = None):
        self.locations_container[location].windprofil(start=start, stop=stop, step=step,
                                                      type=type, v_r=v_r, h_r=h_r, z_0=z_0, a=a)

    def get_v_in_h(self, location, h):
        return self.locations_container[location].df_windprofil.query("h==" + str(h))["v"].values[0]


    def analyse(self, flautenanalyse = True):
        if len(self.locations_container) > 1 and len(self.turbines_container) > 1:
            sys.exit("Mehrere Turbinen und mehrere Standorte. Bitte Auswahl treffen")

        if len(self.locations_container) == 1:
            for turb, turb_obj in self.turbines_container.items():
                # get location_name and location_object of the single location in loc_dict of Analysis object
                loc_name = list(self.locations_container.keys())[0]
                loc_obj = list(self.locations_container.values())[0]
                # document location_name in turbine object and turbine_name in location object
                turb_obj.locations.append(loc_name)
                loc_obj.turbines.append(turb_obj.name)
                # initialize df_main of Analysis object
                df_main = pd.DataFrame()
                df_main['v'] = turb_obj.df_turbine['v']
                df_main['h'] = loc_obj.df_histogramm['h']
                df_main['P'] = turb_obj.df_turbine['P']
                # perform calculations of energy yield
                df_main['E'] = df_main['h'] * df_main['P'] * 8760 / 1000 ** 2 * turb_obj.verfügbarkeit # GWh
                df_main['E_h'] = df_main['E'] / df_main['E'].sum()
                # add rho to data output
                df_main["rho"] = turb_obj.df_turbine["rho"]
                # assign df_main to object
                turb_obj.df_main = df_main
                # Flautenanalyse
                if flautenanalyse:
                    self.flautenanalyse(turb_obj)
                    # add flautenanalyse result to data output
                    turb_obj.df_main["Anzahl der Stunden mit Flaute"] = ''
                    turb_obj.df_main.loc[0, "Anzahl der Stunden mit Flaute"] = turb_obj.flaute
            self.postprocessing()

        elif len(self.locations_container) > 1:
            print("Mehrere Locations")
            for loc, loc_obj in self.locations_container.items():
                # get turbine_name and turbine_object of the single turbine in turbine_dict of Analysis object
                turb_name = list(self.turbines_container.keys())[0]
                turb_obj = list(self.turbines_container.values())[0]
                # document location_name in turbine object and turbine_name in location object
                loc_obj.turbines.append(turb_name)
                turb_obj.locations.append(loc)
                # initialize df_main of Analysis object
                df_main = pd.DataFrame()
                df_main['v'] = turb_obj.df_turbine['v']
                df_main['h'] = loc_obj.df_histogramm['h']
                df_main['P'] = turb_obj.df_turbine['P']
                # perform calculations of energy yield
                df_main['E'] = df_main['h'] * df_main['P'] * 8760 / 1000 ** 2 * turb_obj.verfügbarkeit # GWh
                df_main['E_h'] = df_main['E'] / df_main['E'].sum()
                # assign df_main to object
                loc_obj.df_main = df_main
                # Flautenanalyse
                if flautenanalyse:
                    self.flautenanalyse(loc_obj)
                    # add flautenanalyse result to data output
                    loc_obj.df_main["Anzahl der Stunden mit Flaute"] = ''
                    loc_obj.df_main.loc[0, "Anzahl der Stunden mit Flaute"] = loc_obj.flaute
            self.postprocessing()
        else:
            print("Fehler in analyse()")


    def flautenanalyse(self, obj):
        first_non_zero = obj.df_main["E"].ne(0).idxmax()
        h_sum = obj.df_main["h"].iloc[0:first_non_zero].sum()
        print("Anzahl der Stunden mit Flaute: ", round(h_sum * 8760,2))
        obj.flaute = h_sum * 8760


    def plot(self, selected_plots=["weibull", "messung", "turbine", "main", "ertrag", "ertrag_h", "windprofil"],
             show=True):
        #A = self.analysis_container[analysis]
        fig_list = []

        if "windhistogramm" in selected_plots:
            fig_list.append(plotting.plot_weibull(self.locations_container))
        if "messung" in selected_plots:
            fig_list.append(plotting.plot_messung(self.locations_container))
        if "turbine" in selected_plots:
            fig_list.append(plotting.plot_turbine(self.turbines_container))
        if "main" in selected_plots:
            if len(self.locations_container) == 1:
                for turb in self.turbines_container.values():
                    fig_list.append(plotting.plot_main(turb))
            if len(self.locations_container) > 1:
                for loc in self.locations_container.values():
                    fig_list.append(plotting.plot_main(loc))
        if "ertrag" in selected_plots:
            if len(self.locations_container) == 1:
                fig_list.append(plotting.plot_ertrag(self.turbines_container))
            if len(self.locations_container) > 1:
                fig_list.append(plotting.plot_ertrag(self.locations_container))
        if "ertrag_h" in selected_plots:
            if len(self.locations_container) == 1:
                fig_list.append(plotting.plot_ertrag_h(self.turbines_container))
            if len(self.locations_container) > 1:
                fig_list.append(plotting.plot_ertrag_h(self.locations_container))
        if "windprofil" in selected_plots:
            for loc in self.locations_container.values():
                if loc.df_windprofil is None:
                    continue
                fig_list.append(plotting.plot_windprofil(loc))

        self.fig_list = fig_list

        if show:
            plt.show()


    def postprocessing(self):
        self.pp_data=pd.DataFrame()

        if len(self.locations_container) == 1:
            df_list = []
            loc_obj = list(self.locations_container.values())[0]

            q = pd.DataFrame({loc_obj.name: []})
            df_list.append(q)
            df_list.append(loc_obj.df_histogramm)
            for turb in loc_obj.turbines:
                a = pd.DataFrame({turb:[]})
                df_list.append(a)
                df_list.append(self.turbines_container[turb].df_main)
            self.pp_data = pd.concat(df_list, axis=1)

        if len(self.locations_container) > 1:
            df_list = []
            turb_obj = list(self.turbines_container.values())[0]

            q = pd.DataFrame({turb_obj.name: []})
            df_list.append(q)
            df_list.append(turb_obj.df_turbine)
            for loc in turb_obj.locations:
                a = pd.DataFrame({loc: []})
                df_list.append(a)
                df_list.append(self.locations_container[loc].df_main)
            self.pp_data = pd.concat(df_list, axis=1)

    def save_plots(self, path=""):
        plots_dir = os.path.join(path, "plots")
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
        for fig in self.fig_list:
            fig.savefig(os.path.join(plots_dir, fig.texts[0].get_text() + ".png"))
            # .pdf?

    def save_data(self, path=""):
        Excelwriter = pd.ExcelWriter(os.path.join(path,self.name)+".xlsx", engine="xlsxwriter")
        self.pp_data.to_excel(Excelwriter, sheet_name=self.name, index=False)
        Excelwriter.save()

    def save(self, path=""):
        print('save all')
        windea_dir = os.path.join(path, self.name)
        if not os.path.exists(windea_dir):
            os.makedirs(windea_dir)
        self.save_plots(path=windea_dir)
        self.save_data(path=windea_dir)


class Turbine:

    def __init__(self, name, rho, verfügbarkeit, path=""):
        self.name = name
        self.locations = []
        self.df_turbine = load_turbine(name, path)
        self.df_turbine["P"] *= rho
        self.df_turbine["rho"] *= rho
        self.rho = rho
        self.verfügbarkeit = verfügbarkeit


class Location:

    def __init__(self, name, delta_v = 1, A=None, k=None, v_m=None, type=None, path=""):
        self.name = name
        self.turbines = []
        self.A = A
        self.k = k
        self.v_m = v_m
        self.delta_v = delta_v
        self.type = type
        self.df_windprofil = None
        # weibull oder messung
        if type == "weibull":
            self.df_weibull, self.df_weibull_detailed = weibull.weibull_windhistogramm(A=A, k=k, v_m=v_m, step = delta_v)
            self.df_histogramm = self.df_weibull
        if type == "messung":
            self.df_messung = pd.read_excel(path, engine = 'openpyxl')
            self.df_messung["Frequency"] /= 100
            self.df_histogramm = pd.DataFrame()
            self.df_histogramm['v'] = self.df_messung["to"]

            freq = list(self.df_messung["Frequency"])
            freq.append(0.0)

            freq_mean = []
            for i in range(0, len(freq)):
                freq_mean.append((freq[i] + freq[i+1]) / 2)
                if i == (len(freq) - 2):
                    break

            self.df_histogramm["h"] = freq_mean
            first_row = pd.DataFrame({"v":[0], "h":[0]})
            self.df_histogramm = pd.concat([first_row, self.df_histogramm], ignore_index=True)


    #def windhistogramm(self, A=None, k=None, v_m=None):
    #    self.df_weibull, self.df_weibull_detailed = weibull.weibull_windhistogramm(step = delta_v, A=A, k=k, v_m=v_m)
        # weibull oder messung

    def windprofil(self, start, stop, step, type, v_r, h_r, z_0 = None, a = None):
        df_windprofil = pd.DataFrame()
        h = np.arange(start, stop + step, step)
        df_windprofil['h'] = h

        df_wp_detailed = pd.DataFrame()
        h_detailed = np.arange(start, stop + 0.1, 0.1)
        df_wp_detailed['h_detailed'] = h_detailed

        if type == 'logarithmisch':
            self.windprofil_type = "Logarithmisches Windprofil"
            v = log_windprofil(h_i=h, v_r=v_r, h_r=h_r, z_0=z_0)
            df_windprofil['v'] = v
            v_detailed = log_windprofil(h_i=h_detailed, v_r=v_r, h_r=h_r, z_0=z_0)
            df_wp_detailed['v_detailed'] = v_detailed

        if type == "hellmann":
            self.windprofil_type = "Windprofil aus Potenzgesetz nach Hellmann"
            v = hellmann(h_i=h, v_r=v_r, h_r=h_r, a=a)
            df_windprofil['v'] = v
            v_detailed = hellmann(h_i=h_detailed, v_r=v_r, h_r=h_r, a=a)
            df_wp_detailed['v_detailed'] = v_detailed

        self.df_windprofil = df_windprofil
        self.df_wp_detailed = df_wp_detailed



# Hilfsfunktionen
def log_windprofil(h_i, v_r, h_r, z_0):
    v_i = v_r * (np.log(h_i/z_0, out=np.zeros(h_i.shape, dtype=float), where=h_i!=0) / np.log(h_r/z_0))
    return v_i

def hellmann(v_r, h_r, h_i, a):
    v_i_m = v_r * np.power(h_i / h_r, a)
    return v_i_m

def load_turbine(turbine, path=""):
    if path == "":
        path = os.path.join("data", turbines_dict[turbine])
        data = pkg_resources.resource_string(__name__, path)
    else:
        data = path
    df_turbine = pd.read_excel(data, engine = 'openpyxl', header=2)
    df_turbine["P"] /= df_turbine.loc[0,"rho"]
    df_turbine["rho"] /= df_turbine.loc[0,"rho"]
    return df_turbine