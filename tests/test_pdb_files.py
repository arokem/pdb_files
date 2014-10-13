import os
import tempfile

import numpy as np
import numpy.testing as npt
import scipy.io as sio 

import nibabel as nib
from nibabel.tmpdirs import InTemporaryDirectory


import pdb_files as pdf


def test_pdb():
    """
    Test initialization of the FiberGroup from pdb file

    Benchmark was generated using vistasoft in Matlab as follows:

    >> fg = mtrImportFibers('FG_w_stats.pdb')
    
    """
    pdb_files = ['FG_w_stats.pdb', 'pdb_version2.pdb']
    mat_files = ['fg_from_matlab.mat', 'pdb_version2.mat']
    for ii in range(len(pdb_files)):
        file_name = pdb_files[ii]
        fibers, hdr, fiber_stats, node_stats = pdf.read(file_name)
        # Get the same fiber group as saved in matlab:
        mat_fg = sio.loadmat(mat_files[ii], squeeze_me=True)["fg"]
        k = [d[0] for d in mat_fg.dtype.descr]
        v = mat_fg.item()
        mat_fg_dict = dict(zip(k,v))
        npt.assert_equal(fibers[0].T, mat_fg_dict["fibers"][0])
        if ii==0:
            npt.assert_equal(node_stats[0]["eccentricity"],
                             mat_fg_dict["params"][0].item()[-1][0])

            pdf.write(fibers, hdr, fiber_stats, node_stats, 'pdb_file.pdb')
            fibers2, hdr2, fiber_stats2, node_stats2 = pdf.read('pdb_file.pdb')
            for p1, p2 in zip([fibers, hdr, fiber_stats, node_stats],
                          [fibers2, hdr2, fiber_stats2, node_stats2]):
                npt.assert_equal(p1, p2)
