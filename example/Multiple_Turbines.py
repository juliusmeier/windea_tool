from windea_tool import main

r = main.Windea(name="Multiple Turbines")

r.add_turbine("Enercon E-115 (3000 kW)", rho=1.225, verfügbarkeit = 0.99)
r.add_turbine("Enercon E-70 (2300 kW)", rho=1.225, verfügbarkeit = 0.97)

r.add_location(name="Berlin", type="weibull",
               k=2, v_m=10, delta_v = 1,
               type_windprofil = "logarithmisch", h_r = 10, v_r = 5, z_0 = 2, h = 10
               )
# Turbinen müssen gleiche Hubheight haben
# windprofil funktioniert nur für weibull

# rho, verfügbarkeit
# turbine importieren, interne Datenbank
# weibull(A,k,v_m), messung importieren
# Windprofil: logarithmisch, hellmann: h_r, v_r, z_0/a, h
    # delta_v, start, stop, step
# flautenanalyse = True
# show=True, selected_plots

r.analyse(flautenanalyse = False)

r.plot(show = False)

r.save()
