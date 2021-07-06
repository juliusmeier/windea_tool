from windea_tool import main

# add own turbine via path, windprofil function, flautenanalyse, sort windhistogramm erstellen to Location class
# Windprofil, Nabenhöhe?
# calculate and print general Kennzahlen (P, E_ges, ...)

r = main.Windea(name="Analysis 1")
r.add_turbine("Enercon E-115 (3000 kW)")
r.add_turbine("Enercon E-33 (330 kW)")
# / muss genutzt werden, bei \ muss r vor string
#r.add_turbine("E-200", path="C:/Users/meinm/Documents/Git/windea-tool/example/Enercon_E-30_200kW.xlsx")


# Windprofil: für Location wird k,A,v_m benötigt. Falls diese Parameter nur in einer anderen Höhe
# als Nabenhöhe vorhanden sind, muss das Windprofil genutzt werden nach log oder hellmann
# mit windprofil() v_m aus Nabenhöhe zurückgeben lassen, nutzer muss dann selbst eine variable definieren, die
# add_location() übergeben wird, plot und Daten werden gespeichert und ausgegeben.
# zu location class hinzu???



r.add_location(k=2, v_m=10, name="Dresden", type="weibull")
#r.add_location(k=3, v_m=8, name="Berlin", type="weibull")


r.add_windprofil(location="Dresden", start=0, stop=160, step=10,
                #type='logarithmisch', v_r=5, h_r=10, z_0=0.3)
                type="hellmann", v_r=5, h_r=10, a = 0.25)
#x = r.get_v_in_h(location="Dresden", h=10)
#print(x)
#from windea_tool import plotting
#plotting.plot_windprofil(r.locations_container['Dresden'])

#print(r.locations_container['Dresden'].get_v_in_h(10))



r.analyse()

r.plot(show=False)

r.save()
