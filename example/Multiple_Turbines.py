from windea_tool import main

r = main.Windea(name="Multiple Turbines")

r.add_turbine("Enercon E-115 (3000 kW)", rho=1.225)
r.add_turbine("Enercon E-70 (2300 kW)", rho=1.225, verfügbarkeit = 0.97)

r.add_location(k=2, v_m=10, delta_v = 1,
               h_r = 10, h = 10, type_windprofil = "logarithmisch", v_r = 5, z_0 = 2,
               name="Berlin", type="weibull")

# Windprofil
#r.add_windprofil(location="Dresden", start=0, stop=160, step=10,
                #type='logarithmisch', v_r=5, h_r=10, z_0=0.3)
                #type="hellmann", v_r=5, h_r=10, a = 0.25)



r.analyse()

r.plot(show=False)

r.save()
