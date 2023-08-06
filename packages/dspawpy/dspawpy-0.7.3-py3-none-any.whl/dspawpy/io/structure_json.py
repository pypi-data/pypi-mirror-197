# -*- coding: utf-8 -*-

from typing import Dict,List
import json

import numpy as np
from pymatgen.core import Structure

from .utils import get_lines_without_comment

def from_dspaw_atominfo(atominfo)->Structure:
    lattice = np.asarray(atominfo["Lattice"]).reshape(3,3)
    elements = []
    positions = []
    for atom in atominfo["Atoms"]:
        elements.append(atom["Element"])
        positions.extend(atom["Position"])

    coords = np.asarray(positions).reshape(-1,3)
    is_direct = atominfo["CoordinateType"] == "Direct"
    return Structure(lattice,elements,coords,coords_are_cartesian = (not is_direct))

def from_dspaw_as(as_file)->Structure:
    lines = get_lines_without_comment(as_file,"#")

    N = int(lines[1])
    lattice = []
    for line in lines[3:6]:
        vector = line.split()
        lattice.extend([float(vector[0]),float(vector[1]),float(vector[2])])

    lattice = np.asarray(lattice).reshape(3,3)
    is_direct = line[6].strip() == "Direct"
    elements = []
    positions = []
    for i in range(N):
        atom = lines[i + 7].strip().split()
        elements.append(atom[0])
        positions.extend([float(atom[1]),float(atom[2]),float(atom[3])])

    coords = np.asarray(positions).reshape(-1,3)
    return Structure(lattice,elements,coords,coords_are_cartesian = (not is_direct))

def from_hzw(hzw_file)->Structure:
    lines = get_lines_without_comment(hzw_file, "%")
    number_of_probes = int(lines[0])
    if number_of_probes != 0:
        raise ValueError("dspaw only support 0 probes hzw file")
    lattice = []
    for line in lines[1:4]:
        vector = line.split()
        lattice.extend([float(vector[0]),float(vector[1]),float(vector[2])])

    lattice = np.asarray(lattice).reshape(3,3)
    N = int(lines[4])
    elements = []
    positions = []
    for i in range(N):
        atom = lines[i + 5].strip().split()
        elements.append(atom[0])
        positions.extend([float(atom[1]),float(atom[2]),float(atom[3])])

    coords = np.asarray(positions).reshape(-1,3)
    return Structure(lattice, elements, coords, coords_are_cartesian=True)

def from_dspaw_atominfos(atominfos:List[Dict])->List[Structure]:
    structures = []
    for atominfo in atominfos:
        structures.append(from_dspaw_atominfo(atominfo))
    return structures

def to_dspaw_as(structure:Structure,filename:str,coords_are_cartesian=True):
    with open(filename,"w",encoding="utf-8") as file:
        file.write("Total number of atoms\n")
        file.write("%d\n"%len(structure))

        file.write("Lattice\n")
        for v in structure.lattice.matrix:
            file.write("%.6f %.6f %.6f\n"%(v[0],v[1],v[2]))

        if coords_are_cartesian:
            file.write("Cartesian\n")
        else:
            file.write("Direct\n")
        for site in structure:
            coords = site.coords if coords_are_cartesian else site.frac_coords
            file.write("%s %.6f %.6f %.6f\n"%(site.species_string,coords[0],coords[1],coords[2]))

def to_hzw(structure:Structure,filename:str):
    with open(filename,"w",encoding="utf-8") as file:
        file.write("% The number of probes \n")
        file.write("0\n")
        file.write("% Uni-cell vector\n")

        for v in structure.lattice.matrix:
            file.write("%.6f %.6f %.6f\n"%(v[0],v[1],v[2]))

        file.write("% Total number of device_structure\n")
        file.write("%d\n" % len(structure))
        file.write("% Atom site\n")

        for site in structure:
            file.write("%s %.6f %.6f %.6f\n"%(site.species_string,site.coords[0],site.coords[1],site.coords[2]))


def to_dspaw_dict(structure:Structure,coords_are_cartesian=True)->Dict:
    lattice = structure.lattice.matrix.flatten().tolist()
    atoms = []
    for site in structure:
        coords = site.coords if coords_are_cartesian else site.frac_coords
        atoms.append({"Element":site.species_string,
                      "Position":coords.tolist()
        })

    coordinate_type = "Cartesian" if coords_are_cartesian else "Direct"
    return {"Lattice":lattice,
            "CoordinateType":coordinate_type,
            "Atoms":atoms
    }

def to_dspaw_json(structure:Structure,filename:str,coords_are_cartesian=True):
    d = to_dspaw_dict(structure,coords_are_cartesian)
    with open(filename,"w",encoding="utf-8") as file:
        json.dump(d,file,indent=4)


def to_file(structure:Structure,filename:str,fmt,coords_are_cartesian = True):
    """

    Args:
        structure:
        filename:
        fmt: support "json","as","hzw"
        coords_are_cartesian:

    """
    if fmt == "json":
        to_dspaw_json(structure,filename,coords_are_cartesian)
    elif fmt == "as":
        to_dspaw_as(structure,filename,coords_are_cartesian)
    elif fmt == "hzw":
        to_hzw(structure,filename)

def to_pdb(structures:List[Structure],pdb_filename:str):
    with open(pdb_filename,"w",encoding="utf-8") as file:
        for i,s in enumerate(structures):
            file.write("MODEL         %d\n"%(i+1))
            file.write("REMARK   Converted from Structures\n")
            file.write("REMARK   Converted using dspawpy\n")
            lengths = s.lattice.lengths
            angles = s.lattice.angles
            file.write('CRYST1{0:9.3f}{1:9.3f}{2:9.3f}{3:7.2f}{4:7.2f}{5:7.2f}\n'.format(lengths[0],lengths[1],lengths[2],
                                                                                        angles[0],angles[1],angles[2]))
            for j,site in enumerate(s):
                file.write('%4s%7d%4s%5s%6d%4s%8.3f%8.3f%8.3f%6.2f%6.2f%12s\n'%("ATOM",j+1,site.species_string,"MOL",1,
                                                                                '    ',site.coords[0],
                                                                                site.coords[1],site.coords[2],
                                                                                1.0,0.0,site.species_string))
            file.write("TER\n")
            file.write("ENDMDL\n")

