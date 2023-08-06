# -*- coding: utf-8 -*-
import os
import json
from typing import List

from pymatgen.core import Structure

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from dspawpy.io.structure import to_file
from dspawpy.diffusion.pathfinder import IDPPSolver
class NEB:
    """

    Args:
        initial_structure:
        final_structure:
        nimages: number of images,contain initial and final structure
    """
    def __init__(self,initial_structure,final_structure,nimages):
        """

        Args:
            initial_structure:
            final_structure:
            nimages: number of images,contain initial and final structure
        """

        self.nimages = nimages
        self.iddp = IDPPSolver.from_endpoints(endpoints=[initial_structure, final_structure], nimages=self.nimages - 2)

    def linear_interpolate(self):
        return self.iddp.structures

    def idpp_interpolate(
        self,
        maxiter=1000,
        tol=1e-5,
        gtol=1e-3,
        step_size=0.05,
        max_disp=0.05,
        spring_const=5.0,
    ):
        """

        Args:
            maxiter:
            tol:
            gtol:
            step_size:
            max_disp:
            spring_const:

        Returns:

        """
        return self.iddp.run(maxiter,tol,gtol,step_size,max_disp,spring_const)

def write_neb_structures(structures:List[Structure],coords_are_cartesian = True,fmt:str="json",path:str=".",prefix="structure"):
    """

    Args:
        structures: list of structures
        coords_are_cartesian:
        fmt: support "json","as","poscar","hzw"
        path: output path
        prefix: structure prefix name if fmt != "poscar"

    """
    N = len(str(len(structures)))
    if N <= 2:
        N = 2
    for i,structure in enumerate(structures):
        path_name = str(i).zfill(N)
        os.makedirs(os.path.join(path,path_name),exist_ok=True)
        if fmt == "poscar":
            structure.to(fmt="poscar",filename = os.path.join(path,path_name,"POSCAR"))
        else:
            filename = os.path.join(path,path_name, "%s%s.%s"%(prefix,path_name,fmt))
            to_file(structure,filename,coords_are_cartesian=coords_are_cartesian,fmt=fmt)


def plot_neb_barrier(neb_json):
    with open(neb_json,"r") as file:
        neb = json.load(file)
    try:
        reaction_coordinate = neb["BarrierInfo"]["ReactionCoordinate"]
        energy = neb["BarrierInfo"]["TotalEnergy"]
    except: # old version
        reaction_coordinate = neb["Distance"]["ReactionCoordinate"]
        energy = neb["Energy"]["TotalEnergy"]
    x = [0] # initialize x, to keep the length of x and y equal
    for c in reaction_coordinate:
        if len(x) > 0:
            x.append(x[-1] + c)
        else:
            x.append(c)

    y = [x-energy[0] for x in energy]
    inter_f = interp1d(x,y,kind="cubic")
    xnew = np.linspace(x[0],x[-1],100)
    ynew = inter_f(xnew)

    plt.plot(xnew,ynew,c="b")
    plt.scatter(x,y,c="r")
    plt.xlabel("Reaction Coordinate")
    plt.ylabel("Energy")
    #plt.show()

def plot_neb_converge(neb_json,image_key="01"):
    """

    Args:
        neb_json: neb.json filename
        image_key: image key 01,02,03...

    Returns:
            subplot left ax,right ax
    """
    with open(neb_json,"r") as file:
        neb_total = json.load(file)
    try:
        neb = neb_total["LoopInfo"][image_key]
    except:
        neb = neb_total["Iteration"][image_key]
    maxforce = []
    total_energy = []
    for n in neb:
        maxforce.append(n["MaxForce"])
        total_energy.append(n["TotalEnergy"])

    maxforce = np.array(maxforce)
    total_energy = np.array(total_energy)

    #maxforce = maxforce - maxforce[0]

    x = np.arange(len(neb))

    force = maxforce
    energy = total_energy

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(x,force,label="Max Force",c="black")
    ax1.set_xlabel("Number of ionic step")
    ax1.set_ylabel("Force")
    ax1.set_yscale('log')

    ax2 = ax1.twinx()
    ax2.plot(x,energy,label="Energy",c="r")
    ax2.set_xlabel("Number of ionic step")
    ax2.set_ylabel("Energy")

    fig.legend(loc=1, bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
    return ax1,ax2