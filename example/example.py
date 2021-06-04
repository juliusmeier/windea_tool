import matplotlib.pyplot as plt
from windea_tool import main


r = main.Windea()
r.add_turbine("Enercon E-115 (3000 kW)")
r.add_turbine("Enercon E-33 (330 kW)")


r.add_location(k=2, v_m=10, name="Location 1")

r.t()
r.windhistogramm(k=2, v_m=10)

#r.ertrag()
#print(r.turbines_container)


r.plot_all()
r.save_plots()

r.save_data()

plt.show()