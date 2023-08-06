"""AIMD开始后，指定原子、元素、步数等生成轨迹
当h5和json文件同时存在时，优先读取json文件中的数据
"""

# 1. 读取

import numpy as np


def _parse_indices(index: str, total_step) -> list:
    """解析用户输入的原子序号字符串

    输入：
        - index: 用户输入的原子序号/元素字符串，例如 '1:3,5,7:10'
    输出：
        - indices: 解析后的原子序号列表，例如 [1,2,3,4,5,6,7,8,9,10]
    """
    assert ":" in index, "如果不想切片索引，请输入整数或者列表"
    blcs = index.split(",")
    indices = []
    for blc in blcs:
        if ":" in blc:  # 切片
            low = blc.split(":")[0]
            if not low:
                low = 1  # 从1开始
            else:
                low = int(low)
                assert low > 0, "索引从1开始！"
            high = blc.split(":")[1]
            if not high:
                high = total_step
            else:
                high = int(high)
                assert high <= total_step, "索引超出范围！"

            for i in range(low, high + 1):
                indices.append(i)
        else:  # 单个数字
            indices.append(int(blc))
    return indices


def _read_h5(
    hpath: str,
    index: int or list or str = None,
    ele: str or list or np.array = None,
    ai: int or list or np.array = None,
):
    """从hpath指定的路径读取h5文件中的数据

    输入:
    - hpath: h5文件路径
    - index: 运动轨迹中的第几步，从1开始计数
        如果要切片，用字符串写法： '1, 10:20, 23'
    - ele: 元素，例如 'C'，'H'，'O'，'N'
    - ai: 原子序号（体系中的第几个原子，不是质子数）
        如果要切片，用字符串写法： '1, 10:20, 23'

    输出：
    - Nstep: 总共要保存多少步的信息, int
    - elements: 元素列表, list, Natom x 1
    - positions: 原子位置, list, Nstep x Natom x 3
    - lattices: 晶胞, list, Nstep x 3 x 3
    """
    import h5py

    hf = h5py.File(hpath)  # 加载h5文件
    Total_step = len(np.array(hf.get("/Structures"))) - 2  # 总步数

    if ele and ai:
        raise ValueError("暂不支持同时指定元素和原子序号")
    # 步数
    if index:
        if isinstance(index, int):  # 1
            indices = [index]

        elif isinstance(index, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            indices = index

        elif isinstance(index, str):  # ':', '-3:'
            indices = _parse_indices(index, Total_step)

        else:
            raise ValueError("请输入正确格式的index")

        Nstep = len(indices)
    else:
        Nstep = Total_step
        indices = list(range(1, Nstep + 1))

    # 读取元素列表，这个列表不会随步数改变，也不会“合并同类项”
    from dspawpy.io.utils import get_ele_from_h5

    Elements = get_ele_from_h5(hpath)

    # 开始读取晶胞和原子位置
    lattices = []  # Nstep x 3 x 3
    location = []
    if ele:  # 如果用户指定元素
        if isinstance(ele, str):  # 单个元素符号，例如 'Fe'
            ele_list = list(ele)
            location = np.where(Elements == ele_list)[0]
        # 多个元素符号组成的列表，例如 ['Fe', 'O']
        elif isinstance(ele, list) or isinstance(ele, np.ndarray):
            for e in ele:
                loc = np.where(Elements == e)[0]
                location.append(loc)
            location = np.concatenate(location)
        else:
            raise TypeError("请输入正确的元素或元素列表")
        elements = Elements[location]

    elif ai:  # 如果用户指定原子序号
        if isinstance(ai, int):  # 1
            ais = [ai]
        elif isinstance(ai, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            ais = ai
        elif isinstance(ai, str):  # ':', '-3:'
            ais = _parse_indices(ai, Total_step)
        else:
            raise ValueError("请输入正确格式的ai")
        ais = [i - 1 for i in ais]  # python从0开始计数，但是用户从1开始计数
        elements = Elements[ais]
        location = ais

    else:  # 如果都没指定
        elements = Elements
        location = list(range(len(Elements)))

    # Nstep x Natom x 3
    positions = np.empty(shape=(len(indices), len(elements), 3))
    for i, index in enumerate(indices):  # 步数
        lats = np.array(hf.get("/Structures/Step-" + str(index) + "/Lattice"))
        lattices.append(lats)
        # [x1,x2,...],[y1,y2,...],[z1,z2,...]
        # 结构优化时输出的都是分数坐标，不管CoordinateType写的是啥！
        spos = np.array(hf.get("/Structures/Step-" + str(index) + "/Position"))
        # wrap into [0,1)
        wrapped_spos = spos - np.floor(spos)
        for j, sli in enumerate(location):
            positions[i, j, :] = np.dot(wrapped_spos[:, sli], lats)

    lattices = np.array(lattices)

    return Nstep, elements, positions, lattices


def _read_json(
    jpath: str,
    index: int or list or str = None,
    ele: str or list or np.array = None,
    ai: int or list or np.array = None,
):
    """从json指定的路径读取数据

    输入:
    - jpath: json文件路径
    - ai: 原子序号（体系中的第几个原子，不是质子数）
    - ele: 元素，例如 'C'，'H'，'O'，'N'
    - index: 运动轨迹中的第几步，从1开始

    输出：
    - Nstep: 总共要保存多少步的信息, int
    - elements: 元素列表, list, Natom x 1
    - positions: 原子位置, list, Nstep x Natom x 3
    - lattices: 晶胞, list, Nstep x 3 x 3
    """
    import json

    with open(jpath, "r") as f:
        data = json.load(f)  # 加载json文件

    Total_step = len(data["Structures"])  # 总步数

    if ele and ai:
        raise ValueError("暂不支持同时指定元素和原子序号")
    # 步数
    if index:
        if isinstance(index, int):  # 1
            indices = [index]

        elif isinstance(index, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            indices = index

        elif isinstance(index, str):  # ':', '-3:'
            indices = _parse_indices(index, Total_step)

        else:
            raise ValueError("请输入正确格式的index")

        Nstep = len(indices)
    else:
        Nstep = Total_step
        indices = list(range(1, Nstep + 1))  # [1,Nstep+1)

    # 预先读取全部元素的总列表，这个列表不会随步数改变，也不会“合并同类项”
    # 这样可以避免在循环内部频繁判断元素是否符合用户需要

    Nele = len(data["Structures"][0]["Atoms"])  # 总元素数量
    total_elements = np.empty(shape=(Nele), dtype="str")  # 未合并的元素列表
    for i in range(Nele):
        element = data["Structures"][0]["Atoms"][i]["Element"]
        total_elements[i] = element

    # 开始读取晶胞和原子位置
    # 在data['Structures']['%d' % index]['Atoms']中根据元素所在序号选择结构
    if ele:  # 用户指定要某些元素
        location = []
        if isinstance(ele, str):  # 单个元素符号，例如 'Fe'
            ele_list = list(ele)
        # 多个元素符号组成的列表，例如 ['Fe', 'O']
        elif isinstance(ele, list) or isinstance(ele, np.ndarray):
            ele_list = ele
        else:
            raise TypeError("请输入正确的元素或元素列表")
        for e in ele_list:
            location.append(np.where(total_elements == e)[0])
        location = np.concatenate(location)

    elif ai:  # 如果用户指定原子序号，也要据此筛选元素列表
        if isinstance(ai, int):  # 1
            ais = [ai]
        elif isinstance(ai, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            ais = ai
        elif isinstance(ai, str):  # ':', '-3:'
            ais = _parse_indices(ai, Total_step)
        else:
            raise ValueError("请输入正确格式的ai")
        ais = [i - 1 for i in ais]  # python从0开始计数，但是用户从1开始计数
        location = ais
        # read lattices and poses

    else:  # 如果都没指定
        location = list(range(Total_step))

    # 满足用户需要的elements列表
    elements = np.empty(shape=len(location), dtype="str")
    for i in range(len(location)):
        elements[i] = total_elements[location[i]]

    # Nstep x Natom x 3
    positions = np.empty(shape=(len(indices), len(elements), 3))
    lattices = np.empty(shape=(Nstep, 3, 3))  # Nstep x 3 x 3
    for i, index in enumerate(indices):  # 步数
        lat = data["Structures"][index - 1]["Lattice"]
        lattices[i] = np.array(lat).reshape(3, 3)
        for j, sli in enumerate(location):
            positions[i, j, :] = data["Structures"][index - 1]["Atoms"][sli][
                "Position"
            ][:]

    return Nstep, elements, positions, lattices


# 2. 写轨迹文件
def write_xyz_traj(
    h5_path: str = "aimd.h5",
    jpath: str = None,
    ai=None,
    ele=None,
    index=None,
    xyzfile="aimdTraj.xyz",
):
    """保存xyz格式的轨迹文件

    Parameters
    ----------
    h5_path : str
        DSPAW计算完成后保存的h5文件路径
    jpath : str
        DSPAW计算完成后保存的json文件路径
    ai : int
        原子编号列表（体系中的第几号原子，不是质子数）
    ele : str
        元素，例如 'C'，'H'，'O'，'N'
    index : int
        优化过程中的第几步

    Returns
    -------
    xyzfile: str
        写入xyz格式的轨迹文件，默认为aimdTraj.xyz

    Example
    -------
    >>> from dspawpy.analysis.aimd_traj import write_xyz_traj
    >>> write_xyz_traj(h5_path='aimd.h5', ai=[1,2,3], index=1, xyzfile='aimdTraj.xyz')
    """
    if jpath:
        Nstep, eles, poses, lats = _read_json(jpath, index, ele, ai)
    else:
        Nstep, eles, poses, lats = _read_h5(h5_path, index, ele, ai)
    # 写入文件
    with open(xyzfile, "w") as f:
        # Nstep
        for n in range(Nstep):
            # 原子数不会变，就是不合并的元素总数
            f.write("%d\n" % len(eles))
            # lattice
            f.write(
                'Lattice="%f %f %f %f %f %f %f %f %f" Properties=species:S:1:pos:R:3 pbc="T T T"\n'
                % (
                    lats[n, 0, 0],
                    lats[n, 0, 1],
                    lats[n, 0, 2],
                    lats[n, 1, 0],
                    lats[n, 1, 1],
                    lats[n, 1, 2],
                    lats[n, 2, 0],
                    lats[n, 2, 1],
                    lats[n, 2, 2],
                )
            )
            # position and element
            for i in range(len(eles)):
                f.write(
                    "%s %f %f %f\n"
                    % (eles[i], poses[n, i, 0], poses[n, i, 1], poses[n, i, 2])
                )


def write_dump_traj(
    h5_path="aimd.h5",
    jpath=None,
    ai=None,
    ele=None,
    index=None,
    dumpfile="aimdTraj.dump",
):
    """保存为lammps的dump格式的轨迹文件，暂时只支持正交晶胞！

    Parameters
    ----------
    h5_path : str
        DSPAW计算完成后保存的h5文件路径
    jpath : str
        DSPAW计算完成后保存的json文件路径
    ai : int
        原子编号列表（体系中的第几号原子，不是质子数）
    ele : str
        元素，例如 'C'，'H'，'O'，'N'
    index : int
        优化过程中的第几步

    Returns
    -------
    dumpfile: str
        写入xyz格式的轨迹文件，默认为aimdTraj.xyz

    Example
    -------
    >>> from dspawpy.analysis.aimd_traj import write_dump_traj
    >>> write_dump_traj(h5_path='aimd.h5', ai=[1,2,3], index=1, dumpfile='aimdTraj.dump')
    """
    if jpath:
        Nstep, eles, poses, lats = _read_json(jpath, index, ele, ai)
    else:
        Nstep, eles, poses, lats = _read_h5(h5_path, index, ele, ai)

    # 写入文件
    with open(dumpfile, "w") as f:
        for n in range(Nstep):
            box_bounds = _get_lammps_non_orthogonal_box(lats[n])
            f.write("ITEM: TIMESTEP\n%d\n" % n)
            f.write("ITEM: NUMBER OF ATOMS\n%d\n" % (len(eles)))
            f.write("ITEM: BOX BOUNDS xy xz yz xx yy zz\n")
            f.write(
                "%f %f %f\n%f %f %f\n %f %f %f\n"
                % (
                    box_bounds[0][0],
                    box_bounds[0][1],
                    box_bounds[0][2],
                    box_bounds[1][0],
                    box_bounds[1][1],
                    box_bounds[1][2],
                    box_bounds[2][0],
                    box_bounds[2][1],
                    box_bounds[2][2],
                )
            )
            f.write("ITEM: ATOMS type x y z id\n")
            for i in range(len(eles)):
                f.write(
                    "%s %f %f %f %d\n"
                    % (eles[i], poses[n, i, 0], poses[n, i, 1], poses[n, i, 2], i + 1)
                )


def _get_lammps_non_orthogonal_box(lat: np.ndarray):
    """计算用于输入lammps的盒子边界参数

    Parameters
    ----------
    lat : np.ndarray
        常见的非三角3x3矩阵

    Returns
    -------
    box_bounds:
        用于输入lammps的盒子边界
    """
    # https://docs.lammps.org/Howto_triclinic.html
    A = lat[0]
    B = lat[1]
    C = lat[2]
    assert np.cross(A, B).dot(C) > 0, "Lat is not right handed"

    # 将常规3x3矩阵转成标准的上三角矩阵
    alpha = np.arccos(np.dot(B, C) / (np.linalg.norm(B) * np.linalg.norm(C)))
    beta = np.arccos(np.dot(A, C) / (np.linalg.norm(A) * np.linalg.norm(C)))
    gamma = np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B)))

    ax = np.linalg.norm(A)
    a = np.array([ax, 0, 0])

    bx = np.linalg.norm(B) * np.cos(gamma)
    by = np.linalg.norm(B) * np.sin(gamma)
    b = np.array([bx, by, 0])

    cx = np.linalg.norm(C) * np.cos(beta)
    cy = (np.linalg.norm(B) * np.linalg.norm(C) - bx * cx) / by
    cz = np.sqrt(abs(np.linalg.norm(C) ** 2 - cx**2 - cy**2))
    c = np.array([cx, cy, cz])

    # triangluar matrix in lammmps cell format
    # note that in OVITO, it will be down-triangular one
    # lammps_lattice = np.array([a,b,c]).T

    # write lammps box parameters
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=The%20inverse%20relationship%20can%20be%20written%20as%20follows
    lx = np.linalg.norm(a)
    xy = np.linalg.norm(b) * np.cos(gamma)
    xz = np.linalg.norm(c) * np.cos(beta)
    ly = np.sqrt(np.linalg.norm(b) ** 2 - xy**2)
    yz = (np.linalg.norm(b) * np.linalg.norm(c) * np.cos(alpha) - xy * xz) / ly
    lz = np.sqrt(np.linalg.norm(c) ** 2 - xz**2 - yz**2)

    # "The parallelepiped has its “origin” at (xlo,ylo,zlo) and is defined by 3 edge vectors starting from the origin given by a = (xhi-xlo,0,0); b = (xy,yhi-ylo,0); c = (xz,yz,zhi-zlo)."
    # 令原点在(0,0,0)，则 xlo = ylo = zlo = 0
    xlo = ylo = zlo = 0
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=the%20LAMMPS%20box%20sizes%20(lx%2Cly%2Clz)%20%3D%20(xhi%2Dxlo%2Cyhi%2Dylo%2Czhi%2Dzlo)
    xhi = lx + xlo
    yhi = ly + ylo
    zhi = lz + zlo
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=This%20bounding%20box%20is%20convenient%20for%20many%20visualization%20programs%20and%20is%20calculated%20from%20the%209%20triclinic%20box%20parameters%20(xlo%2Cxhi%2Cylo%2Cyhi%2Czlo%2Czhi%2Cxy%2Cxz%2Cyz)%20as%20follows%3A
    xlo_bound = xlo + np.min([0, xy, xz, xy + xz])
    xhi_bound = xhi + np.max([0, xy, xz, xy + xz])
    ylo_bound = ylo + np.min([0, yz])
    yhi_bound = yhi + np.max([0, yz])
    zlo_bound = zlo
    zhi_bound = zhi
    box_bounds = np.array(
        [
            [xlo_bound, xhi_bound, xy],
            [ylo_bound, yhi_bound, xz],
            [zlo_bound, zhi_bound, yz],
        ]
    )

    return box_bounds
