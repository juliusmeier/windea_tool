import math
import numpy as np
import pandas as pd

# hier mit optional arguments, damit eine Funktion für k,A und k,v_m
def weibull(v, A=None, k=2, v_m=None):
    if A is None:
        A = 2/math.sqrt(math.pi) * v_m

    h = k/A * (v/A)**(k-1) * np.exp(-(v/A)**k)

    return h

def weibull_windhistogramm(start=0, stop=30, step=1, A = None, k = 2, v_m = None):
    v = np.arange(start, stop + step, step)
    df = pd.DataFrame(index=v)

    v_detailed = np.arange(start, stop + 0.1, 0.1)
    df_detailed = pd.DataFrame(index=v_detailed)

    h = weibull(v = df.index, A=A, k=k, v_m=v_m)
    df['h'] = h

    h_detailed = weibull(v = df_detailed.index, A=A, k=k, v_m=v_m)
    df_detailed['h_detailed'] = h_detailed

    return df, df_detailed