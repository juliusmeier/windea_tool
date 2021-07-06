import pandas as pd
import matplotlib.pyplot as plt

# Windmessung mit Stufendiagramm
wd = pd.read_excel("windmessung.xlsx", engine = 'openpyxl')
print(wd)

edges = wd['from']
# get last value from the "to" column
last = wd.loc[wd.index[-1],'to']
last = pd.Series(last)
# append last to edges to obey len(edges) == len(values) + 1
edges = edges.append(last, ignore_index=True)

#plt.stairs(values = [1,2,3,2,1], edges = [0,1,2,3,4,5])
plt.stairs(values=wd['Frequency'], edges=edges)
plt.show()

# process messung: v(0,30) -> h(0,30), make it smooth? look at quaschning and wind.ch