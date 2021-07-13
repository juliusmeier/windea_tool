from windea_tool import main

case_study = main.Windea(name="Case Study")

case_study.add_turbine(name="Vestas V126-3.45", rho=1.225, verfügbarkeit=0.98,
                       path = r"Vestas_V126-3.45.xlsx")

case_study.add_location(name="Rostock", type="weibull", k=1.79, A=5.54)
case_study.add_location(name="Naundorf", type="messung", path=r"Windmessung_Naundorf.xlsx")

case_study.analyse(flautenanalyse=True)

case_study.plot(show=False)

case_study.save()