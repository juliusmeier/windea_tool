import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def log_windprofil(h_i, v_r, h_r, z_0):
    v_i = v_r * (np.log(h_i/z_0, out=np.zeros(h_i.shape, dtype=float), where=h_i!=0) / np.log(h_r/z_0))
    return v_i

def hellmann(v_r, h_r, h_i, a):
    v_i_m = v_r * np.power(h_i / h_r, a)
    return v_i_m

def windprofil(start, stop, step, type, v_r, h_r, z_0 = None, a = None):
    df_windprofil = pd.DataFrame()
    h = np.arange(start, stop + step, step)
    df_windprofil['h'] = h

    df_wp_detailed= pd.DataFrame()
    h_detailed = np.arange(start, stop + 0.1, 0.1)
    df_wp_detailed['h_detailed'] = h_detailed

    if type == 'logarithmisch':
        v = log_windprofil(h_i=h, v_r=v_r, h_r=h_r, z_0=z_0)
        df_windprofil['v'] = v
        v_detailed = log_windprofil(h_i=h_detailed, v_r=v_r, h_r=h_r, z_0=z_0)
        df_wp_detailed['v_detailed'] = v_detailed

    if type == "hellmann":
        v = hellmann(h_i=h, v_r=v_r, h_r=h_r, a=a)
        df_windprofil['v'] = v
        v_detailed = hellmann(h_i=h_detailed, v_r=v_r, h_r=h_r, a=a)
        df_wp_detailed['v_detailed'] = v_detailed

    return df_windprofil, df_wp_detailed


df_windprofil, df_wp_detailed = windprofil(start=0, stop=160, step=10,
                                           type='logarithmisch',
                                           v_r=5, h_r=10, z_0=0.3, a = 0.25)

ax = df_windprofil.plot(x='v', y='h', title="Logarithmisches Windprofil",kind="scatter",
                        marker="o", edgecolor="r", color="none")
ax.grid()

ax.plot(df_wp_detailed['v_detailed'],df_wp_detailed['h_detailed'])

plt.xlim(left=0)
plt.ylim(bottom=0)
plt.xlabel("Windgeschwindigkeit in m/s")
plt.ylabel("Höhe in m")
plt.show()


print(df_windprofil)