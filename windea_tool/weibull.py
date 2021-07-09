import math
import numpy as np
import pandas as pd

def weibull(v, A=None, k=2, v_m=None):
    print("A: ",A)
    if A is None:
        A = 2/math.sqrt(math.pi) * v_m
    if v_m is None:
        v_m = round(A * math.sqrt(math.pi) / 2, 2)

    h = k/A * (v/A)**(k-1) * np.exp(-(v/A)**k)

    return h, A, v_m

def weibull_windhistogramm(start=0, stop=30, step = 1, A = None, k = 2, v_m = None):
    v = np.arange(start, stop + step, step)
    df = pd.DataFrame()
    df['v'] = v

    v_detailed = np.arange(start, stop + 0.01, 0.01)
    df_detailed = pd.DataFrame()
    df_detailed['v'] = v_detailed

    h, A, v_m = weibull(v = df['v'], A=A, k=k, v_m=v_m)
    df['h'] = h

    h_detailed, A, v_m = weibull(v = df_detailed['v'], A=A, k=k, v_m=v_m)
    df_detailed['h_detailed'] = h_detailed

    return df, df_detailed, A, v_m