from windea_tool import main

case_study = main.Windea(name="Case Study")

case_study.add_turbine(name="Vestas V126-3.45)", rho=1.225,
                       path = r"C:\Users\meinm\Documents\Git\windea-tool\example\Vestas_V126-3.45.xlsx")

case_study.add_location(name="Rostock", type="weibull", k=1.79, A=5.54)
case_study.add_location(name="Naundorf", type="messung", path=r"C:\Users\meinm\Documents\Git\windea-tool\example\Windmessung_Naundorf.xlsx")

case_study.analyse()

case_study.plot(show=True,)

case_study.save()