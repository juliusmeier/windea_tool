import matplotlib.pyplot as plt
import pandas as pd

colors_dict = {"blue": '#1f77b4', "orange": '#ff7f0e', "green": '#2ca02c', "red": '#d62728',
               "purple": '#9467bd', "brown": '#8c564b', "magenta": '#e377c2', "grey": '#7f7f7f',
               "yellow": '#bcbd22', "cyan": '#17becf',}

#formatting = {"title_size": 20, "labelsize": 14,}

def plot_weibull(location_dict, display_parameters = True):
    weibull = False
    fig, ax = plt.subplots(figsize=(12,6))
    for loc in location_dict.values():
        if loc.df_weibull is not None:
            weibull = True
            parameters = ""
            # get Weibull Parameters
            if display_parameters:
                loc.A = 10
                parameters = "\nA: " + str(loc.A) + ", k: " + str(loc.k) + ", v_m: " + str(loc.v_m)

            loc.df_weibull_detailed.plot(x='v', y="h_detailed", ax=ax,
                                         label = loc.name + parameters)

            ax.set_xlabel("Windgeschwindigkeit in m/s")
            ax.set_ylabel("Relative Häufigkeit")
            ax.set_xlim(left=0)
            ax.set_ylim(bottom=0)

            ax.grid()
            fig.suptitle("Häufigkeitsverteilung der Windgeschwindigkeit", fontsize=20)
    if weibull:
        return fig
    else:
        plt.close(fig)
        return None

def plot_turbine(turbines_container):
    fig, ax = plt.subplots(figsize=(12,6))
    for turb in turbines_container.values():
        turb.df_turbine.plot(x = "v", y = "P", kind="line", marker="o", color="red", ax=ax,
                             label=turb.name)

    ax.legend(loc="lower center")
    ax.set_ylabel("Leistung in kW", fontsize=14)
    ax.set_xlabel("Windgeschwindigkeit in m/s", fontsize=14)
    ax.grid()
    fig.suptitle("Leistungskennlinie", fontsize=20)

    return fig

def plot_main(turb_loc):
    fig,ax = plt.subplots(figsize=(12,6))
    ax.plot(turb_loc.df_main['v'], turb_loc.df_main['h'], color=colors_dict["blue"], marker="o", label="h")
    ax.plot(turb_loc.df_main['v'], turb_loc.df_main['E_h'], color=colors_dict["green"], marker="o", label="E_h")
    ax.set_xlabel("Windgeschwindigkeit in m/s",fontsize=14)
    ax.set_ylabel("Relative Häufigkeit",fontsize=14)
    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    ax2.plot(turb_loc.df_main['v'], turb_loc.df_main['P'],color=colors_dict["red"], marker="o", label="P")
    ax2.set_ylabel("Leistung in kW",fontsize=14)

    plt.xlim(left=0)
    ax.set_ylim(bottom=0,top=0.2)
    ax2.set_ylim(bottom=0,)

    ax.grid()
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")

    fig.suptitle(turb_loc.name, fontsize=20)
    return fig

def plot_ertrag(turbines_container): #https://stackoverflow.com/questions/54714018/horizontal-grid-only-in-python-using-pandas-plot-pyplot
    fig, ax = plt.subplots(figsize=(12,6))
    colors=["blue", "green", "purple", "cyan"]
    i=0

    df = pd.DataFrame()
    for turb, turb_obj in turbines_container.items():
        df[turb] = turb_obj.df_main['E']
        df.set_index(pd.Index(turb_obj.df_main['v']))

    df.plot.bar(ax = ax, color=colors, xlabel="Windgeschwindigkeit in m/s" , ylabel="Windenergieertrag in GWh")

    ax.grid(axis='y')
    ax.set_axisbelow(True)

    fig.suptitle("Ertragsverteilung in GWh", fontsize=20)
    return fig

def plot_ertrag_h(turbines_container, marker="o"):
    fig, ax = plt.subplots(figsize=(12,6))
    colors = ["blue", "green", "purple", "cyan"]
    i=0
    for turb in turbines_container.values():
        turb.df_main.plot(x='v', y='E_h', ax=ax, kind='line', marker=marker, color=colors[i],
            xlabel="Windgeschwindigkeit in m/s" , ylabel="Relative Häufigkeit",
            label=turb.name)
        i+=1
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    fig.suptitle("Häufigkeitsverteilung des Ertrages", fontsize=20)
    return fig


def plot_windprofil(location):
    fig, ax = plt.subplots(figsize=(12,6))
    location.df_windprofil.plot(x='v', y='h', kind="scatter",
                                marker="o", edgecolor="r", color="none", ax=ax)
    ax.grid()

    ax.plot(location.df_wp_detailed['v_detailed'],location.df_wp_detailed['h_detailed'], label=location.name)

    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.xlabel("Windgeschwindigkeit in m/s", fontsize=14)
    plt.ylabel("Höhe in m", fontsize=14)

    plt.legend()
    fig.suptitle(location.windprofil_type + ": " + location.name, fontsize=20)
    
    return fig


def plot_messung(location_dict):
    messung = False
    fig, ax = plt.subplots(figsize=(12, 6))
    for loc in location_dict.values():
        if loc.df_messung is not None:
            messung = True
            edges = loc.df_messung['from']
            # get last value from the "to" column
            last = loc.df_messung.loc[loc.df_messung.index[-1], 'to']
            last = pd.Series(last)
            # append last to edges to obey len(edges) == len(values) + 1
            edges = edges.append(last, ignore_index=True)
            # plt.stairs(values = [1,2,3,2,1], edges = [0,1,2,3,4,5])
            plt.stairs(values=loc.df_messung['Frequency'], edges=edges, label="Messung " + loc.name,
                       color = colors_dict["orange"])

            # lineplot
            loc.df_histogramm.plot(x="v", y="h", ax=ax, color=colors_dict["blue"])

            ax.set_xlabel("Windgeschwindigkeit in m/s")
            ax.set_ylabel("Relative Häufigkeit")
            ax.set_xlim(left=0)
            ax.set_ylim(bottom=0)

            plt.legend()
            ax.grid()
            fig.suptitle("Häufigkeitsverteilung der Windgeschwindigkeit " + loc.name, fontsize=20)
    if messung:
        return fig
    else:
        plt.close(fig)
        return None

def plot_flaute(obj_container):
    fig, ax = plt.subplots(figsize=(12, 6))
    for name, obj in obj_container.items():
        ax.bar(x = obj.name, height = obj.flaute)

    ax.set_ylabel("Anzahl der Stunden mit Flaute")
    ax.set_ylim(bottom=0)

    fig.suptitle("Flautenanalyse", fontsize=20)

    return fig