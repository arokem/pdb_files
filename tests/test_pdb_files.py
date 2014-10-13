import os
import tempfile

import numpy as np
import numpy.testing as npt
import scipy.io as sio 

import nibabel as nib
from nibabel.tmpdirs import InTemporaryDirectory
import dipy.data as dpd

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
            with InTemporaryDirectory():
                pdf.write(fibers, hdr, fiber_stats, node_stats, 'pdb_file.pdb')
                fibers2, hdr2, fiber_stats2, node_stats2 = \
                    pdf.read('pdb_file.pdb')
                for p1, p2 in zip([fibers, hdr, fiber_stats, node_stats],
                                  [fibers2, hdr2, fiber_stats2, node_stats2]):
                    npt.assert_equal(p1, p2)


def test_trk_pdb():
    """

    """
    trk_file = dpd.get_data('fornix')
    trk_fibs, trk_hdr = nib.trackvis.read(trk_file)
    get_fibers = [f[0] for f in trk_fibs]
    with InTemporaryDirectory():
        pdf.trk2pdb(trk_file, 'pdb_file.pdb')
        fibers, hdr, fiber_stats, node_stats = pdf.read('pdb_file.pdb')
        npt.assert_equal(get_fibers, fibers)
        pdf.pdb2trk('pdb_file.pdb', 'new_trk.trk')
        new_trk_fibs, new_trk_hdr = nib.trackvis.read(trk_file)
        npt.assert_equal(trk_fibs, new_trk_fibs)
        npt.assert_equal(trk_hdr, new_trk_hdr)
        
