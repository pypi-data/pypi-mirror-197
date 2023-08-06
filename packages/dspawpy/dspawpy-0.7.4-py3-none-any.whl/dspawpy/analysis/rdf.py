from math import ceil
from multiprocessing import cpu_count
from typing import Dict, List, Tuple, Union
import numpy as np
from joblib import Parallel, delayed
from scipy.ndimage import gaussian_filter1d
from pymatgen.core import Structure
from dspawpy.analysis.aimd_traj import _read_h5
from dspawpy.io.utils import get_ele_from_h5
import matplotlib.pyplot as plt
import os

# modified based on https://github.com/materialsvirtuallab/pymatgen-analysis-diffusion/blob/master/pymatgen/analysis/diffusion/aimd/rdf.py


class RadialDistributionFunctionFast:
    """
    Fast radial distribution analysis.
    """

    def __init__(
        self,
        structures: Union[Structure, List[Structure]],
        rmin: float = 0.0,
        rmax: float = 10.0,
        ngrid: float = 101,
        sigma: float = 0.0,
        n_jobs=None,
    ):
        """
        This method calculates rdf on `np.linspace(rmin, rmax, ngrid)` points.
        Args:
            structures (list of pymatgen Structures): structures to compute RDF
            rmin (float): minimal radius
            rmax (float): maximal radius
            ngrid (int): number of grid points, defaults to 101
            sigma (float): smooth parameter
            n_jobs (int): number of CPUs in processing
        """
        if n_jobs is None:
            n_jobs = 1
        if n_jobs < 0:
            n_jobs = cpu_count()
        self.n_jobs = n_jobs
        if isinstance(structures, Structure):
            structures = [structures]
        self.structures = structures
        # Number of atoms in all structures should be the same
        assert len({len(i) for i in self.structures}) == 1
        elements = [[i.specie for i in j.sites] for j in self.structures]
        unique_elements_on_sites = [
            len(set(i)) == 1 for i in list(zip(*elements))]

        # For the same site index, all structures should have the same element there
        if not all(unique_elements_on_sites):
            raise RuntimeError(
                "Elements are not the same at least for one site")

        self.rmin = rmin
        self.rmax = rmax
        self.ngrid = ngrid

        self.dr = (self.rmax - self.rmin) / \
            (self.ngrid - 1)  # end points are on grid
        self.r = np.linspace(self.rmin, self.rmax, self.ngrid)  # type: ignore

        max_r = self.rmax + self.dr / 2.0  # add a small shell to improve robustness

        if self.n_jobs > 1:
            self.neighbor_lists = Parallel(n_jobs=self.n_jobs)(
                delayed(_get_neighbor_list)(s, max_r) for s in self.structures
            )
        else:
            self.neighbor_lists = [i.get_neighbor_list(
                max_r) for i in self.structures]
        # each neighbor list is a tuple of
        # center_indices, neighbor_indices, image_vectors, distances
        (
            self.center_indices,
            self.neighbor_indices,
            self.image_vectors,
            self.distances,
        ) = list(zip(*self.neighbor_lists))

        elements = np.array([str(i.specie)
                            for i in structures[0]])  # type: ignore
        self.center_elements = [elements[i] for i in self.center_indices]
        self.neighbor_elements = [elements[i] for i in self.neighbor_indices]
        self.density = [{}] * len(self.structures)  # type: List[Dict]

        self.natoms = [i.composition.to_data_dict["unit_cell_composition"]
                       for i in self.structures]

        for s_index, natoms in enumerate(self.natoms):
            for i, j in natoms.items():
                self.density[s_index][i] = j / self.structures[s_index].volume

        self.volumes = 4.0 * np.pi * self.r**2 * self.dr
        self.volumes[self.volumes < 1e-8] = 1e8  # avoid divide by zero
        self.n_structures = len(self.structures)
        self.sigma = ceil(sigma / self.dr)
        # print(elements)

    def _dist_to_counts(self, d):
        """
        Convert a distance array for counts in the bin
        Args:
            d: (1D np.array)
        Returns:
            1D array of counts in the bins centered on self.r
        """
        counts = np.zeros((self.ngrid,))
        indices = np.array(
            np.floor((d - self.rmin + 0.5 * self.dr) / self.dr), dtype=int)

        unique, val_counts = np.unique(indices, return_counts=True)
        counts[unique] = val_counts
        return counts

    def get_rdf(
        self,
        ref_species: Union[str, List[str]],
        species: Union[str, List[str]],
        is_average=True,
    ):
        """
        Args:
            ref_species (list of species or just single specie str): the reference species.
                The rdfs are calculated with these species at the center
            species (list of species or just single specie str): the species that we are interested in.
                The rdfs are calculated on these species.
            is_average (bool): whether to take the average over
                all structures
        Returns:
            (x, rdf) x is the radial points, and rdf is the rdf value.
        """
        if self.n_jobs > 1:
            all_rdfs = Parallel(n_jobs=self.n_jobs)(
                self.get_one_rdf(ref_species, species, i) for i in range(self.n_structures)
            )
            all_rdfs = [i[1] for i in all_rdfs]
        else:
            all_rdfs = [self.get_one_rdf(ref_species, species, i)[
                1] for i in range(self.n_structures)]
        if is_average:
            all_rdfs = np.mean(all_rdfs, axis=0)
        return self.r, all_rdfs

    def get_one_rdf(
        self,
        ref_species: Union[str, List[str]],
        species: Union[str, List[str]],
        index=0,
    ):
        """
        Get the RDF for one structure, indicated by the index of the structure
        in all structures
        Args:
            ref_species (list of species or just single specie str): the reference species.
                The rdfs are calculated with these species at the center
            species (list of species or just single specie str): the species that we are interested in.
                The rdfs are calculated on these species.
            index (int): structure index in the list
        Returns:
            (x, rdf) x is the radial points, and rdf is the rdf value.
        """
        if isinstance(ref_species, str):
            ref_species = [ref_species]

        if isinstance(species, str):
            species = [species]

        indices = (
            (np.isin(self.center_elements[index], ref_species))
            & (np.isin(self.neighbor_elements[index], species))
            & (self.distances[index] >= self.rmin - self.dr / 2.0)
            & (self.distances[index] <= self.rmax + self.dr / 2.0)
            & (self.distances[index] > 1e-8)
        )

        density = sum(self.density[index][i] for i in species)
        natoms = sum(self.natoms[index][i] for i in ref_species)
        distances = self.distances[index][indices]
        counts = self._dist_to_counts(distances)
        rdf_temp = counts / density / self.volumes / natoms
        if self.sigma > 1e-8:
            rdf_temp = gaussian_filter1d(rdf_temp, self.sigma)
        return self.r, rdf_temp

    def get_coordination_number(self, ref_species, species, is_average=True):
        """
        returns running coordination number
        Args:
            ref_species (list of species or just single specie str): the reference species.
                The rdfs are calculated with these species at the center
            species (list of species or just single specie str): the species that we are interested in.
                The rdfs are calculated on these species.
            is_average (bool): whether to take structural average
        Returns:
            numpy array
        """
        # Note: The average density from all input structures is used here.
        all_rdf = self.get_rdf(ref_species, species, is_average=False)[1]
        if isinstance(species, str):
            species = [species]
        density = [sum(i[j] for j in species) for i in self.density]
        cn = [np.cumsum(rdf * density[i] * 4.0 * np.pi * self.r**2 * self.dr)
              for i, rdf in enumerate(all_rdf)]
        if is_average:
            cn = np.mean(cn, axis=0)
        return self.r, cn


def _get_neighbor_list(structure, r) -> Tuple:
    """
    Thin wrapper to enable parallel calculations
    Args:
        structure (pymatgen Structure): pymatgen structure
        r (float): cutoff radius
    Returns:
        tuple of neighbor list
    """
    return structure.get_neighbor_list(r)


def get_Structures(aimdh5: str = 'aimd.h5'):
    """get pymatgen structures from aimd.h5 file
    """
    Nstep, elements, positions, lattices = _read_h5(aimdh5)
    strs = []
    for i in range(Nstep):
        strs.append(Structure(lattices[i], elements, positions[i], coords_are_cartesian=True))
    return strs


def get_rdf_xy(filepath, ele1, ele2):
    """--> r(x-axis), s_na_rdf(y-axis)
    """
    if filepath.endswith('.json'):
        from monty.serialization import loadfn
        # Parse the DiffusionAnalyzer object from json file directly
        obj = loadfn(filepath)
        structure_list = []
        for i, s in enumerate(obj.get_drift_corrected_structures()):
            structure_list.append(s)
            if i == 9:
                break
    elif filepath.endswith('.h5'):
        # create Structure structure_list from aimd.h5
        structure_list = get_Structures(filepath)
    else:
        raise ValueError("File format not supported")

    obj = RadialDistributionFunctionFast(
        structures=structure_list, ngrid=101, rmax=10.0, sigma=0.1)

    r, s_na_rdf = obj.get_rdf(ele1, ele2)
    return r, s_na_rdf


def rdf_analysis(datafile:str or list, ele1:str or list, ele2:str or list, figname:str=None, show:bool=True):
    """AIMD计算后分析rdf并画图

    Parameters
    ----------
    datafile : str or list of str
        aimd.h5或aimd.json文件路径或包含这两个文件之一的目录；
        写成列表的话将依次读取数据并合并到一起
    select : list
        元素类别序号列表，如[0]，默认为None，即计算所有原子
        暂不支持计算多个元素的rdf
    rdf_type : str
        计算rdf的类型，可选xyz,xy,xz,yz,x,y,z，默认为None，即计算所有分量
    figname : str
        图片名称，默认为None，即不保存图片
    show : bool
        是否显示图片，默认为True

    Returns
    -------
    rdf分析后的图片

    Examples
    --------
    >>> from dspawpy.analysis.rdf import rdf_analysis
    >>> rdf_analysis(datafile='aimd.h5', ele1='H', ele2='O', figname='rdf.png', show=True)
    # 也可以同时指定多个元素对，如C-O, H-N
    >>> rdf_analysis(datafile='aimd.h5', ele1=['C','H'], ele2=['O','N'], figname='rdf.png', show=True)
    """
    # 寻找数据源文件
    dfs = []
    if isinstance(datafile, list): # 续算模式
        for df in datafile:
            if df.endswith(".h5") or df.endswith(".json"):
                df = df
            elif os.path.exists(os.path.join(df, 'aimd.h5')):
                df = os.path.join(df, 'aimd.h5')
            elif os.path.exists(os.path.join(df, 'aimd.json')):
                df = os.path.join(df, 'aimd.json')
            else:
                raise FileNotFoundError("不存在相应的aimd.h5或aimd.json文件！")
            dfs.append(df)
    else: # 单次计算模式
        if datafile.endswith(".h5") or datafile.endswith(".json"):
            df = datafile
        elif os.path.exists(os.path.join(datafile, 'aimd.h5')):
            df = os.path.join(datafile, 'aimd.h5')
        elif os.path.exists(os.path.join(datafile, 'aimd.json')):
            df = os.path.join(datafile, 'aimd.json')
        else:
            raise FileNotFoundError("不存在相应的aimd.h5或aimd.json文件！")
        dfs.append(df)

    # 开始分析数据
    if isinstance(ele1, list) and isinstance(ele2, list):
        assert len(ele1) == len(ele2), '元素列表长度不相等！'
        for i in range(len(ele1)): # 每个元素对
            xs = []
            ys = []
            for df in dfs: # 合并多个数据源
                if i == 0:
                    print(f'Reading {os.path.abspath(df)}...')
                x, y = get_rdf_xy(df, ele1[i], ele2[i])
                xs.append(x)
                ys.append(y)
            
            xs = np.arange(len(np.array(xs).flatten()))
            ys = np.array(ys).flatten()
            plt.plot(xs, ys, label=r'$g_{\alpha\beta}(r)$' + f'[{ele1[i]},{ele2[i]}]')

    else:
        assert isinstance(ele1, str) and isinstance(ele2, str), 'ele1和ele2应皆为字母或字母列表！'
        xs = []
        ys = []
        for df in dfs:
            x, y = get_rdf_xy(df, ele1, ele2)
            xs.append(x)
            ys.append(y)
        xs = np.arange(len(np.array(xs).flatten()))
        ys = np.array(ys).flatten()
        plt.plot(xs, ys, label=r'$g_{\alpha\beta}(r)$' + f'[{ele1},{ele2}]')

    plt.xlabel(r"$r$"+"(Å)")
    plt.ylabel(r"$g(r)$")
    plt.legend()

    if figname:
        plt.savefig(figname)
        print(f'图片已保存到 {os.path.abspath(figname)}')
    if show: # 画子图的话，不应每个子图都show
        plt.show() # show会自动清空图片

