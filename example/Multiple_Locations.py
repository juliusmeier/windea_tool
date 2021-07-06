from windea_tool import main

a = main.Windea(name="Multiple Locations")

a.add_turbine("Enercon E-115 (3000 kW)", rho=1.225)

a.add_location(name="Berlin", type="messung", path = r"C:\Users\meinm\Documents\Git\windea-tool\example\windmessung_template.xlsx")
a.add_location(k=3, v_m=8, name="Dresden", type="weibull")

a.analyse()

a.plot(show=True)

a.save()
