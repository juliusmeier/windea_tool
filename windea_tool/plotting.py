import matplotlib.pyplot as plt

# besser: colors_dict mit y-Wert als key
colors_dict = {"blue": '#1f77b4', "orange": '#ff7f0e', "green": '#2ca02c', "red": '#d62728',
               "purple": '#9467bd', "brown": '#8c564b', "magenta": '#e377c2', "grey": '#7f7f7f',
               "yellow": '#bcbd22', "cyan": '#17becf',}

formatting = {"title_size": 20, "labelsize": 14,} # marker, figsize

def plot_weibull(location):
    fig, ax = plt.subplots()
    location.df_weibull_detailed.plot(y="h_detailed", ax=ax,
                                      legend=False)

    ax.set_xlabel("Windgeschwindigkeit in m/s")
    ax.set_ylabel("Relative Häufigkeit")
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    parameters = {"A: " : location.A, "k: " : location.k, "v_m: " : location.v_m}
    for key, value in dict(parameters).items():
        if value is None:
            del parameters[key]
    text=""
    for key, value in parameters.items():
        text += key + str(value) + ", "
    text = text[:-2]
    print(text)
    plt.text(  # position text relative to Axes https://riptutorial.com/matplotlib/example/16030/coordinate-systems-and-text
        0.95, 0.95, text,
        ha='right', va='top',
        transform=ax.transAxes,
        bbox=dict(facecolor='white', edgecolor='black', alpha=1)
    )

    ax.grid()
    fig.suptitle("Häufigkeitsverteilung der Windgeschwindigkeit", fontsize=20)

    return fig

def plot_turbine(turbines_container):
    fig, ax = plt.subplots() # figsize=(12,5)
    for turb in turbines_container:
        turb.df_turbine.plot(x = "v", y = "P", kind="line", marker="o", color="red", ax=ax, label=turb.turbine_name)

    ax.set_ylabel("Leistung in kW", fontsize=14)
    ax.set_xlabel("Windgeschwindigkeit in m/s", fontsize=14)
    ax.grid()
    fig.suptitle("Leistungskennlinie", fontsize=20)

    return fig

def plot_main(turbine):
    # create figure and axis objects with subplots()
    fig,ax = plt.subplots()
    # make a plot
    ax.plot(turbine.df_main['v'], turbine.df_main['h'], color=colors_dict["blue"], marker="o", label="h")
    ax.plot(turbine.df_main['v'], turbine.df_main['E_h'], color=colors_dict["green"], marker="o", label="E_h")
    # set x-axis label
    ax.set_xlabel("Windgeschwindigkeit in m/s",fontsize=14)
    # set y-axis label
    ax.set_ylabel("Relative Häufigkeit",fontsize=14)
    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(turbine.df_main['v'], turbine.df_main['P'],color=colors_dict["red"], marker="o", label="P")
    ax2.set_ylabel("Leistung in kW",fontsize=14)

    plt.xlim(left=0)
    ax.set_ylim(bottom=0,top=0.2)
    ax2.set_ylim(bottom=0,)

    ax.grid()
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")

    fig.suptitle(turbine.turbine_name, fontsize=20)
    return fig

def plot_ertrag(turbines_container, ylabel, title, color, figsize=None): #https://stackoverflow.com/questions/54714018/horizontal-grid-only-in-python-using-pandas-plot-pyplot
    fig, ax = plt.subplots(figsize=figsize)
    colors=["blue", "green"]
    i=0
    for turb in turbines_container:
        turb.df_main.plot(x='v', y='E', ax=ax, kind='bar', color=colors[i],
                          xlabel="Windgeschwindigkeit in m/s" , ylabel=ylabel,
                          label=turb.turbine_name)
        i += 1
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    fig.suptitle(title, fontsize=20)
    return fig

def plot_ertrag_h(turbines_container, marker="o"):
    fig, ax = plt.subplots()
    colors = ["blue", "green"]
    i=0
    for turb in turbines_container:
        turb.df_main.plot(x='v', y='E_h', ax=ax, kind='line', marker=marker, color=colors[i],
            xlabel="Windgeschwindigkeit in m/s" , ylabel="Relative Häufigkeit",
            label=turb.turbine_name)
        i+=1
    ax.grid(axis='y')
    ax.set_axisbelow(True)

    fig.suptitle("Häufigkeitsverteilung des Ertrages", fontsize=20)
    return fig