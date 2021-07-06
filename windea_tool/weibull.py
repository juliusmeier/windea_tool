import math
import numpy as np
import pandas as pd

# move to Location class and always set all Parameters (show all in plot)

# hier mit optional arguments, damit eine Funktion für k,A und k,v_m
def weibull(v, A=None, k=2, v_m=None):
    if A is None:
        A = 2/math.sqrt(math.pi) * v_m

    h = k/A * (v/A)**(k-1) * np.exp(-(v/A)**k)

    return h

def weibull_windhistogramm(start=0, stop=30, step = 1, A = None, k = 2, v_m = None):
    v = np.arange(start, stop + step, step)
    df = pd.DataFrame()
    df['v'] = v

    v_detailed = np.arange(start, stop + 0.01, 0.01)
    df_detailed = pd.DataFrame()
    df_detailed['v'] = v_detailed

    h = weibull(v = df['v'], A=A, k=k, v_m=v_m)
    df['h'] = h

    h_detailed = weibull(v = df_detailed['v'], A=A, k=k, v_m=v_m)
    df_detailed['h_detailed'] = h_detailed

    return df, df_detailed