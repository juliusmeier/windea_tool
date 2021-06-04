import matplotlib.pyplot as plt
from windea_tool import main
from windea_tool import plotting
from windea_tool import weibull
# pkg: pandas, numpy, matplotlib, openpyxl, xlsxwriter ,setuptools,
# $ pip install git+https://github.com/<github username>/roman
#pip install openpyxl
# set engine parameter to "openpyxl"pd.read_excel(path, engine = 'openpyxl')

# 2 Turbinen vergleichen!! Default darstellung von main und customize zulassen

#w = weibull(v, k=2, v_m=10) # [k,v_m]
#w = weibull(v,v_m=10)       # [k=2,v_m]
#w = weibull(v, A=11, k=1.5) # [A,k]


"""
df, df_detailed = weibull.weibull_windhistogramm(k=2, v_m=10)

en = main.load_turbine('Enercon E-115 (3000 kW)')
en2 = main.load_turbine('Enercon E-33 (330 kW)')


main.ertrag(df, en)

fig_list = []
fig_list.append(plotting.plot_weibull(df_detailed))
fig_list.append(plotting.plot_turbine(en, en2))
fig_list.append(plotting.plot_main(df))
fig_list.append(plotting.plot_ertrag(df, ylabel="Windenergieertrag in GWh",
                                   title="Ertragsverteilung in GWh", color="blue"))
fig_list.append(plotting.plot_ertrag_h(df))

#print(fig_list[0].axes[0].get_title())
#print(fig_list[0].texts[0].get_text())

#main.save_plots(fig_list=fig_list)
#main.save_data(en)
#plt.show()
"""

r = main.Windea()
print(r.df_main)
#r.add_turbine("Enercon E-33 (330 kW)")
r.add_turbine("Enercon E-115 (3000 kW)")
print(r.df_turbine)
r.windhistogramm(k=2, v_m=10)
print(r.df_weibull)
r.ertrag()
print(r.df_main)
r.plot_all()
r.save_plots()

#r.save_data()

#plt.show()


"""
# Windmessung mit Stufendiagramm
wd = pd.read_excel("../windea_tool/data/wind_dist.xlsx", engine = 'openpyxl')
#print(wd)
y = wd['Frequency']
#plt.stairs(values = [1,2,3,2,1], edges = [0,1,2,3,4,5])
#plt.show()
"""



