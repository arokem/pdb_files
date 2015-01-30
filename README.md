# The PDB file format: pathway data-bases for tractography solutions

Based on work by Sherbondy, Dougherty, Wandell and others in the [Stanford VISTA lab](http://vistalab.stanford.edu/).

This library implements reading and writing of .pdb tractography files.

It also includes command-line interfaces to convert pdb files from/to trk
files, which are used as follows:

    pdb2trk pdb_file.pdb trk_file.trk

And:

    trk2pdb trk_file.trk pdb_file.pdb    


## Installation

### Dependencies:

This software depends on [numpy](http://www.numpy.org/) and on nibabel. To
install these dependencies, the easiest route is to install the [Anaconda](https://store.continuum.io/cshop/anaconda/) python distribution and then use `pip` to install nibabel:

     pip install nibabel
 
To install the software itself, [download](https://github.com/vistalab/pdb_files/archive/master.zip) the source code and run:

    python setup.py install

### Installing with pip

To install the release version of `pdb_files` using `pip`, you can run:

    pip install pdb_files
  

## File format specification:

The following is the nominal specification of PDB files, version 3. Note that
some of these things were not implemented in practice in many files, so the
code implements a partial version of this spec.

```
 The file-format is organized as a semi-hierarchical data-base, according to
    the following specification:
    [ header size] - int
    -- HEADER FOLLOWS --
    [4x4 xform matrix ] - 16 doubles
    [ number of pathway statistics ] - int
    for each statistic:
        [ currently unused ] - bool
        [ is stat stored per point, or aggregate per path? ] - bool
        [ currently unused ] - bool
        [ name of the statistic ] - char[255]
        [ currently unused ] - char[255]
        [ unique ID - unique identifier for this stat across files ] - int

    ** The algorithms bit is not really working as advertised: **
    [ number of algorithms ] - int
    for each algorithm:
       [ algorithm name ] - char[255]
       [ comments about the algorithm ] - char[255]
       [ unique ID -  unique identifier for this algorithm, across files ] - int

    [ version number ] - int
    -- HEADER ENDS --
    [ number of pathways ] - int
    [ pts per fiber ] - number of pathways integers
    for each pathway:
       [ header size ] - int
       -- PATHWAY HEADER FOLLOWS --
        ** The following are not actually encoded in the fiber header and are
         currently set in an arbitrary fashion: **
       [ number of points ] - int
       [ algorithm ID ] - int
       [ seed point index ] - int

       for each statistic:
          [ precomputed statistical value ] - double
       -- PATHWAY HEADER ENDS --
       for each point:
            [ position of the point ] - 3 doubles (ALREADY TRANSFORMED from
                                                   voxel space!)
          for each statistic:
             IF computed per point (see statistics header, second bool field):
             for each point:
               [ statistical value for this point ] - double

```



