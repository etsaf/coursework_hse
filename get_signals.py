import numpy as np
import pandas as pd

#filename - название файла, записанного оксиметром, r_1 и r_2 - расстояния между источниками и приемником
def get_signals(filename, r_1, r_2, lmbd_1, lmbd_2): #lmbd_1 и lmbd_2 - длины волн источников
    df = pd.read_excel(filename)
    dc_1 = df["DC 1 A"].values # сигнал, записанный для lmbd2, r1
    dc_3 = df["DC 3 A"].values # lmbd2, r2
    dc_5 = df["DC 5 A"].values # lmbd1, r1
    dc_7 = df["DC 7 A"].values # lmbd1, r2
    time = df["Time"].values # временные отметки измерений
    eps_hhb = {692: 4.7564, 834: 1.7891} #табличные значения для возможных длин волн
    eps_hbo = {692: 0.9558, 834: 2.3671}
    sl = dict() # значения Sl_DC
    sl[lmbd_1] = (np.log(dc_7 / dc_5) + 2 * np.log(r_2 / r_1)) / (r_2 - r_1)
    sl[lmbd_2] = (np.log(dc_3 / dc_1) + 2 * np.log(r_2 / r_1)) / (r_2 - r_1)
    sto2 = (eps_hhb[lmbd_1] - eps_hhb[lmbd_2] * np.square(sl[lmbd_1] / sl[lmbd_2])) * 100
    sto2 /= ((eps_hhb[lmbd_1] - eps_hbo[lmbd_1]) - (eps_hhb[lmbd_2] - eps_hbo[lmbd_2]) * \
                    np.square(sl[lmbd_1] / sl[lmbd_2]))
    dpf = 5.9 # табличное значение
    d_mua_1 = (1 / (r_1 * dpf)) * np.log(dc_1[0] / dc_1)
    d_mua_3 = (1 / (r_2 * dpf)) * np.log(dc_3[0] / dc_3)
    d_mua_lmbd2 = (d_mua_1 + d_mua_3) / 2
    d_mua_5 = (1 / (r_1 * dpf)) * np.log(dc_5[0] / dc_5)
    d_mua_7 = (1 / (r_2 * dpf)) * np.log(dc_7[0] / dc_7)
    d_mua_lmbd1 = (d_mua_5 + d_mua_7) / 2
    d_hbo = (d_mua_lmbd2 * eps_hhb[lmbd_1] - d_mua_lmbd1 * eps_hhb[lmbd_2]) / \
    (eps_hbo[lmbd_2] * eps_hhb[lmbd_1] - eps_hbo[lmbd_1] * eps_hhb[lmbd_2]) * 1000
    d_hhb = (d_mua_lmbd1 * eps_hbo[lmbd_2] - d_mua_lmbd2 * eps_hbo[lmbd_1]) / \
    (eps_hbo[lmbd_2] * eps_hhb[lmbd_1] - eps_hbo[lmbd_1] * eps_hhb[lmbd_2]) * 1000
    d_thb = d_hbo + d_hhb
    d_hb = d_hbo - d_hhb
    return sto2, d_hb, d_hbo, d_hhb, d_thb, time, d_mua_lmbd1, d_mua_lmbd2