import os
import tempfile

import numpy as np
import numpy.testing as npt
import scipy.io as sio 

import nibabel as nib
from nibabel.tmpdirs import InTemporaryDirectory


import pdb_files as pdb


def test_fg_from_pdb():
    """
    Test initialization of the FiberGroup from pdb file

    Benchmark was generated using vistasoft in Matlab as follows:

    >> fg = mtrImportFibers('FG_w_stats.pdb')
    
    """
    pdb_files = ['FG_w_stats.pdb', 'pdb_version2.pdb']
    mat_files = ['fg_from_matlab.mat', 'pdb_version2.mat']
    for ii in range(len(pdb_files)):
        file_name = pdb_files[ii]
        fg = pdb.read(file_name)
        # Get the same fiber group as saved in matlab:
        mat_fg = sio.loadmat(mat_files[ii], squeeze_me=True)["fg"]
        k = [d[0] for d in mat_fg.dtype.descr]
        v = mat_fg.item()
        mat_fg_dict = dict(zip(k,v))
        npt.assert_equal(fg.name, mat_fg_dict["name"])
        npt.assert_equal(fg.fibers[0].coords, mat_fg_dict["fibers"][0])
        if ii==0:
            npt.assert_equal(fg.fibers[0].node_stats["eccentricity"],
                         mat_fg_dict["params"][0].item()[-1][0])

        pdb.write(fg, 'fg_new.pdb')
    
    
def test_pdb_from_fg():
    """
    Test writing a fiber-group to file
    """
    coords1 = np.arange(900).reshape(3,300)
    coords2 = np.arange(900).reshape(3,300) + 100

    fiber_stats = dict(foo=1, bar=2)
    node_stats = dict(ecc=np.arange(300))


    fg = mtf.FiberGroup([mtf.Fiber(coords1,
                                   fiber_stats=fiber_stats,
                                   node_stats=node_stats),
                         mtf.Fiber(coords2,
                                   fiber_stats=fiber_stats,
                                   node_stats=node_stats)])

    temp_dir = tempfile.gettempdir()

    pdb.pdb_from_fg(fg, os.path.join(temp_dir,'fg.pdb'))

    # Test that the properties are preserved upon reloading: 
    fg2 = pdb.fg_from_pdb(os.path.join(temp_dir,'fg.pdb'))

    npt.assert_equal(fg2[0].coords, fg[0].coords)
    npt.assert_equal(fg2[1].coords, fg[1].coords)

    npt.assert_equal(fg2[0].node_stats, fg[0].node_stats)
    npt.assert_equal(fg2[1].node_stats, fg[1].node_stats)
    
    npt.assert_equal(fg2.fiber_stats, fg.fiber_stats)

def test_pdb_trk():
    """
    Test reading of trk files into a FiberGroup
    """
    # This is a trk file taken from the dipy distro: 
    trk_file = 'tracks300.trk'
    fg = pdb.fg_from_trk(trk_file)
    # It has 300 fibers in it:
    npt.assert_equal(len(fg.fibers), 300)
    # It has a bogus affine (singular), so we should get np.eye(4)
    npt.assert_equal(fg.affine, np.eye(4))
