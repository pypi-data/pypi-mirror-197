# -*- coding: utf-8 -*-
import json
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.interpolate import interp1d

def plot_potential_along_axis(data,axis=2,smooth=False,smooth_frac=0.8,**kwargs):
    all_axis = [0,1,2]
    all_axis.remove(axis)
    y = np.mean(data,tuple(all_axis))
    x = np.arange(len(y))
    if smooth:
        s = sm.nonparametric.lowess(y, x, frac=smooth_frac)
        plt.plot(s[:,0], s[:,1], label="macroscopic average",**kwargs)

    plt.plot(x,y,label="planar electrostatic",**kwargs)
    return plt

def plot_optical(optical_json:str,key:str,index:int=0):
    """

    Args:
        optical_json: optical.json filename
        key: "AbsorptionCoefficient","ExtinctionCoefficient","RefractiveIndex","Reflectance"
        index:

    Returns:

    """
    with open(optical_json,"r") as file:
        data_all = json.load(file)

    energy = data_all["OpticalInfo"]["EnergyAxe"]
    data = data_all["OpticalInfo"][key]
    data = np.asarray(data).reshape(len(energy),6)[:,index]

    inter_f = interp1d(energy, data, kind="cubic")
    energy_spline = np.linspace(energy[0],energy[-1],2001)
    data_spline = inter_f(energy_spline)

    plt.plot(energy_spline,data_spline,c="b")
    plt.xlabel("Photon energy (eV)")
    plt.ylabel("%s %s"%(key,r"$\alpha (\omega )(cm^{-1})$"))





