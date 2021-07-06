from windea_tool import main

r = main.Windea(name="Multiple Locations")

r.add_turbine("Enercon E-115 (3000 kW)", rho=1.225)


r.add_location(name="Berlin", type="messung", path = r"C:\Users\meinm\Documents\Git\windea-tool\example\windmessung.xlsx")
r.add_location(k=3, v_m=8, name="Dresden", type="weibull")


r.analyse(flautenanalyse = True)

r.plot(show=True, selected_plots=["flautenanalyse"])

r.save()

