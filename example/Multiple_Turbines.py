from windea_tool import main

r = main.Windea(name="Multiple Turbines")

r.add_turbine("Enercon E-115 (3000 kW)", rho=1.225)
r.add_turbine("Enercon E-70 (2300 kW)", rho=1.225, verfügbarkeit = 0.97)

r.add_location(k=2, v_m=10, delta_v = 1,
               h_r = 10, h = 10, type_windprofil = "logarithmisch", v_r = 5, z_0 = 2,
               name="Berlin", type="weibull")

# rho, verfügbarkeit
# turbine importieren, interne Datenbank
# weibull(A,k,v_m), messung importieren
# Windprofil: logarithmisch, hellmann: h_r, v_r, z_0/a, h
    # delta_v, start, stop, step
# flautenanalyse = True
# show=True, selected_plots



r.analyse(flautenanalyse=True)

r.plot(show=True)

r.save()
