from windea_tool import main

case_study = main.Windea(name="Case Study")

case_study.add_turbine(name="Vestas V112 (3000 kW)", rho=1.225,
                       path = r"C:\Users\meinm\Documents\Git\windea-tool\example\Vestas_V112_3000kW.xlsx")

case_study.add_location(name="Berlin", type="weibull", k=2.04, A=6.66)

case_study.analyse()

case_study.plot(show=True)

case_study.save()