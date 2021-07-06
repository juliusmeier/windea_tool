from windea_tool import main

# Minimal Beispiel mit Leistungskennlinie aus interner Datenbank
a = main.Windea(name="Analysis_1")

a.add_turbine(name="Enercon E-115 (3000 kW)", rho=1.225)

a.add_location(name="Hamburg", type="weibull", k=3, v_m=8)

a.analyse()

a.plot(show=False)

a.save()


# Änderung der Dichte und der Verfügbarkeit, importieren von Messdaten und Leistungskennlinie
b = main.Windea(name="Analysis_2")

b.add_turbine(name="Vestas V112 (3000 kW)", rho=1.1, verfügbarkeit=0.97,
              path = r"C:\Users\meinm\Documents\Git\windea-tool\example\Vestas_V112_3000kW.xlsx")

b.add_location(name="Hamburg", type="messung", path = r"C:\Users\meinm\Documents\Git\windea-tool\example\windmessung_template.xlsx")

b.analyse()

b.plot(show=False)

b.save()


# Nutzen des logarithmischen Windprofils, um die Windgeschwindigkeit in einer anderen Höhe für die Erstellung
# des Windhistogramms zu nutzen. Nur ausgewählte Plots sollen gespeichert werden.
c = main.Windea(name="Analysis_3")

c.add_turbine(name="Vestas V112 (3000 kW)", rho=1.225,
              path = r"C:\Users\meinm\Documents\Git\windea-tool\example\Vestas_V112_3000kW.xlsx")

c.add_location(name="Berlin", type="weibull",
               k=2, v_m=8, delta_v = 1,
               type_windprofil = "logarithmisch", h_r = 10, v_r = 5, z_0 = 2, h = 10)

c.analyse()

c.plot(show=False, selected_plots=["main", "windhistogramm", "windprofil"])

c.save()
