from typing import List, Union
import numpy as np
from pymatgen.core.structure import Structure
from dspawpy.io.structure import from_dspaw_atominfos
from dspawpy.io.utils import get_ele_from_h5
import matplotlib.pyplot as plt
import os

# Mean Squared Displacement.  see  https://docs.mdanalysis.org/2.0.0/documentation_pages/analysis/msd.html#
class MSD:
    def __init__(self, structures: List[Structure], select: Union[str, List[int]] = "all", msd_type='xyz'):
        self.structures = structures
        self.msd_type = msd_type

        self.n_frames = len(structures)
        if select == "all":
            self.n_particles = len(structures[0])
        else:
            self.n_particles = len(select)
        self.lattice = structures[0].lattice

        self._parse_msd_type()

        self._position_array = np.zeros(
            (self.n_frames, self.n_particles, self.dim_fac))

        if select == "all":
            for i, s in enumerate(self.structures):
                self._position_array[i, :, :] = s.frac_coords[:, self._dim]
        else:
            for i, s in enumerate(self.structures):
                self._position_array[i, :,
                                     :] = s.frac_coords[select, :][:, self._dim]

    def _parse_msd_type(self):
        r""" Sets up the desired dimensionality of the MSD.

        """
        keys = {'x': [0], 'y': [1], 'z': [2], 'xy': [0, 1],
                'xz': [0, 2], 'yz': [1, 2], 'xyz': [0, 1, 2]}

        self.msd_type = self.msd_type.lower()

        try:
            self._dim = keys[self.msd_type]
        except KeyError:
            raise ValueError(
                'invalid msd_type: {} specified, please specify one of xyz, '
                'xy, xz, yz, x, y, z'.format(self.msd_type))

        self.dim_fac = len(self._dim)

    def run(self):
        result = np.zeros((self.n_frames, self.n_particles))

        rd = np.zeros((self.n_frames, self.n_particles, self.dim_fac))
        for i in range(1, self.n_frames):
            disp = self._position_array[i, :, :] - \
                self._position_array[i - 1, :, :]
            # mic by periodic boundary condition
            disp[np.abs(disp) > 0.5] = disp[np.abs(disp) > 0.5] - \
                np.sign(disp[np.abs(disp) > 0.5])
            disp = np.dot(disp, self.lattice.matrix)
            rd[i, :, :] = disp
        rd = np.cumsum(rd, axis=0)
        for n in range(1, self.n_frames):
            disp = rd[n:, :, :] - rd[:-n, :, :]  # [n:-n] window
            sqdist = np.square(disp).sum(axis=-1)
            result[n, :] = sqdist.mean(axis=0)

        return result.mean(axis=1)

def msd_analysis(datafile:str, select:list=None, msd_type:str=None, timestep:float=None, figname:str=None, show:bool=True, ax=None):
    """AIMD计算后分析MSD并画图

    Parameters
    ----------
    datafile : str
        aimd.h5或aimd.json文件或包含这两个文件之一的目录
    select : list
        元素类别序号列表，如[0]，默认为None，即计算所有原子
        暂不支持计算多个元素的MSD
    msd_type : str
        计算MSD的类型，可选xyz,xy,xz,yz,x,y,z，默认为None，即计算所有分量
    timestep : float
        时间间隔，单位为fs，默认1.0fs
    figname : str
        图片名称，默认为None，即不保存图片
    show : bool
        是否显示图片，默认为True
    ax: matplotlib axes object
        用于将图片绘制到matplotlib的子图上

    Returns
    -------
    MSD分析后的图片

    Examples
    --------
    >>> from dspawpy.analysis.msd import msd_analysis
    >>> msd_analysis(datafile='aimd.h5', select=[0], msd_type='xyz', figname='msd.png', show=True)
    # 如果不指定select和msd_type，则计算所有原子的所有分量
    """
    # 参数初始化
    if not select:
        select = "all"
    if not msd_type:
        msd_type = "xyz"
    if not timestep:
        timestep = 1.0

    # 寻找数据源文件
    if datafile.endswith(".h5") or datafile.endswith(".json"):
        df = datafile
    elif os.path.exists(os.path.join(datafile, 'aimd.h5')):
        df = os.path.join(datafile, 'aimd.h5')
    elif os.path.exists(os.path.join(datafile, 'aimd.json')):
        df = os.path.join(datafile, 'aimd.json')
    else:
        raise FileNotFoundError("不存在相应的aimd.h5或aimd.json文件！")
    
    # 开始分析数据
    print(f'Reading {os.path.abspath(df)}...')
    structures = from_dspaw_atominfos(aimd_dir=df)
    eles = get_ele_from_h5(hpath=df) # get element list
    eles = list(set(eles)) # remove duplicate elements
    eles.sort() # sort element types alphabetically

    msd = MSD(structures, select, msd_type)
    result = msd.run()

    if isinstance(select, list):
        s = select[0]
        lb = f'{eles[s]}'
    else:
        lb = 'all atoms'

    # Plot
    nframes = msd.n_frames
    lagtimes = np.arange(nframes) * timestep  # make the lag-time axis

    if ax:
        ax.plot(lagtimes, result, c="black", ls="-", label=lb)
        ax.legend()
    else:
        fig, ax = plt.subplots()
        ax.plot(lagtimes, result, c="black", ls="-", label=lb)
        ax.set_xlabel("Time (fs)")
        ax.set_ylabel("MSD (Å)")
        ax.legend()
    if figname:
        plt.savefig(figname)
    if not ax and show: # 画子图的话，不应每个子图都show
        plt.show() # show会自动清空图片

    return ax