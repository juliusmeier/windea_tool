import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windea_tool import test
# pkg: pandas, numpy, matplotlib, openpyxl, setuptools
# $ pip install git+https://github.com/<github username>/roman
test.print_hello()

# hier mit optional arguments, damit eine Funktion für k,A und k,v_m
def weibull(k,v_m, v_i):
    A = 2/math.sqrt(math.pi) * v_m
    print(A)
    print(type(v_i))
    h_i = k/A * (v_i/A)**(k-1) * np.exp(-(v_i/A)**k)
    return h_i

v_i = np.arange(0, 35, 1)
#print(v_i)


w= weibull(2,10,v_i)
#print(type(w), w)

df = pd.DataFrame(index=v_i)
df["h_i"] = w
#print(df)
#df.plot()
#plt.show()

def windprofil(h_i, v_r, h_r, z_0 ):
    v_i = v_r * (np.log(h_i/z_0) / np.log(h_r/z_0))
    return v_i

h_i = np.arange(10, 160, 10)
v = windprofil(h_i=h_i, v_r=5, h_r=10, z_0=0.1)
df2 = pd.DataFrame({'h':h_i})
df2['v']= v
#print(df2)
#df2.plot(x='v', y='h')
#plt.show()

#pip install openpyxl
# set engine parameter to "openpyxl"pd.read_excel(path, engine = 'openpyxl')
en33 = pd.read_excel("../windea_tool/data/Enercon_E-33.xlsx", engine = 'openpyxl')
#print(type(en33))
#print(en33)

wd = pd.read_excel("../windea_tool/data/wind_dist.xlsx", engine = 'openpyxl')
#print(wd)
y = wd['Frequency']

plt.stairs(values = [1,2,3,2,1], edges = [0,1,2,3,4,5])
plt.show()

def load_turbine():
    return pd.read_excel('data/Enercon_E-33.xlsx', engine = 'openpyxl')

