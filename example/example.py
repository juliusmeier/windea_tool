import matplotlib.pyplot as plt
from windea_tool import main


r = main.Windea()
r.add_turbine("Enercon E-115 (3000 kW)")
r.add_turbine("Enercon E-33 (330 kW)")

r.add_location(k=2, v_m=10, location_name="Location 1")
r.add_location(k=3, v_m=8, location_name="Berlin")


#r.analyse(name="Analysis 1")
#r.analyse(loc="Location 1" , turb=["Enercon E-115 (3000 kW)","Enercon E-33 (330 kW)"], name="Analysis 1")
r.analyse(loc=["Location 1", "Berlin"], turb="Enercon E-115 (3000 kW)", name="Analysis E-115")


#r.postprocessing_1(analysis = "Analysis 1")
#r.save_data(analysis = "Analysis 1")
r.postprocessing_2(analysis="Analysis E-115")
r.save_data(analysis="Analysis E-115")

#r.plot_analysis(analysis="Analysis 1")
r.plot_analysis(analysis="Analysis E-115")

#r.save_plots()#
plt.show()