import collections.abc as collections
import os
from typing import Any, Union, Sequence

import ovito
from ..data import DataCollection
from ..pipeline import Pipeline, FileSource
from ..nonpublic import PipelineStatus, FileImporter, PythonScriptFileImporter

def import_file(location: Union[str, os.PathLike, Sequence[str]], **params: Any) -> Pipeline:
    """ Imports data from an external file.

        This Python function corresponds to the *Load File* menu command in OVITO's
        user interface. The format of the imported file is automatically detected (see :ref:`list of supported formats <manual:file_formats.input>`).
        Depending on the file's format, additional keyword parameters may be required
        to specify how the data should be interpreted. These keyword parameters are documented below.

        :param str|os.PathLike|Sequence[str] location: The file(s) to import. This can be a local file path or a remote *sftp://* or *https://* URL.
        :param params: Additional keyword parameters to be passed to the file reader. See below and the documentation of :ref:`individual file readers <manual:file_formats.input>` for format-specific options.
        :returns: The new :py:class:`~ovito.pipeline.Pipeline` that has been created for the imported data.

        The function creates and returns a new :py:class:`~ovito.pipeline.Pipeline` object, which uses the contents of the
        external data file as input. The pipeline will be wired to a :py:class:`~ovito.pipeline.FileSource`, which
        reads the input data from the external file and passes it on to the pipeline. You can access the
        data by calling the :py:meth:`Pipeline.compute() <ovito.pipeline.Pipeline.compute>` method or, alternatively,
        :py:meth:`FileSource.compute() <ovito.pipeline.FileSource.compute>` on the data :py:attr:`~ovito.pipeline.Pipeline.source`.
        As long as the new :py:class:`~ovito.pipeline.Pipeline` contains no modifiers yet, both methods will return the same data.

        Note that the :py:class:`~ovito.pipeline.Pipeline` is not automatically inserted into the three-dimensional scene.
        That means the loaded data won't appear in rendered images or the interactive viewports of OVITO by default.
        For that to happen, you need to explicitly insert the pipeline into the scene by calling its :py:meth:`~ovito.pipeline.Pipeline.add_to_scene` method if desired.

        Furthermore, note that you can re-use the returned :py:class:`~ovito.pipeline.Pipeline` if you want to load a different
        data file later on. Instead of calling :py:func:`!import_file` again to load another file,
        you can use the :py:meth:`pipeline.source.load(...) <ovito.pipeline.FileSource.load>` method to replace the input file
        of the already existing pipeline.

        .. _import_file.file_columns:

        **File data columns**

        When importing simple-format XYZ files or legacy *binary* LAMMPS dump files, the mapping of file columns
        to particle properties in OVITO must be specified using the ``columns`` keyword parameter::

            pipeline = import_file('file.xyz', columns =
                ['Particle Identifier', 'Particle Type', 'Position.X', 'Position.Y', 'Position.Z'])

        The number of column strings must match the actual number of data columns in the input file.
        See this :ref:`table <particle-properties-list>` for standard particle property names. Alternatively, you can specify
        user-defined names for file columns that should be read as custom particle properties by OVITO.
        For vector properties, the component name must be appended to the property's base name as demonstrated for the ``Position`` property in the example above.
        To ignore a file column during import, use ``None`` as entry in the ``columns`` list.

        For LAMMPS dump files or extended-format XYZ files, OVITO automatically determines a reasonable column-to-property mapping, but you may override it using the
        ``columns`` keyword. This can make sense, for example, if the file columns containing the particle coordinates
        do not follow the standard naming scheme ``x``, ``y``, and ``z`` (as is the case when importing time-averaged atomic positions computed by LAMMPS, for example).

        .. _import_file.frame_sequence:

        **Frame sequences**

        OVITO automatically detects if the imported file contains multiple data frames (timesteps).
        Alternatively (and additionally), it is possible to load a sequence of files in the same directory by using the ``*`` wildcard character
        in the filename. Note that ``*`` may appear only once, only in the filename component of the path, and only in place of numeric digits.
        Furthermore, it is possible to pass an explicit list of file paths to the :py:func:`!import_file` function, which will be loaded
        as an animatable sequence. All variants can be combined. For example, to load two file sets from different directories as one
        consecutive sequence::

           import_file('sim.xyz')     # Load all frames contained in the given file
           import_file('sim.*.xyz')   # Load 'sim.0.xyz', 'sim.100.xyz', 'sim.200.xyz', etc.
           import_file(['sim_a.xyz', 'sim_b.xyz'])  # Load an explicit list of snapshot files
           import_file(['dir_a/sim.*.xyz',
                        'dir_b/sim.*.xyz']) # Load several file sequences from different directories

        The number of frames found in the input file(s) is reported by the :py:attr:`~ovito.pipeline.FileSource.num_frames` attribute of the pipeline's :py:class:`~ovito.pipeline.FileSource`
        You can step through the frames with a ``for``-loop as follows:

        .. literalinclude:: ../example_snippets/import_access_animation_frames.py

        .. _import_file.lammps_atom_style:

        **LAMMPS atom style**

        When loading a LAMMPS data file, the atom style may have to be specified using the ``atom_style`` keyword parameter unless the file contains
        a hint string, which allows OVITO to detect the style automatically. Data files written by the LAMMPS ``write_data`` command or by OVITO contain such a hint, for example.
        For data files not containing a hint, the atom style must be specified explicitly as in these examples::

           import_file('full_model.data', atom_style = 'full')
           import_file('hybrid_model.data', atom_style = 'hybrid', atom_substyles = ('template', 'charge'))

        .. _import_file.particle_ordering:

        **Particle ordering**

        Particles are read and stored by OVITO in the same order as they are listed in the input file.
        Some file formats contain unique particle identifiers or tags which allow OVITO to track individual particles
        over time even if the storage order changes from frame to frame. OVITO will automatically make use of that
        information where appropriate without touching the original storage order. However, in some situations it may be
        desirable to explicitly have the particles sorted with respect to the IDs. You can request this
        reordering by passing the ``sort_particles=True`` option to :py:func:`!import_file`. Note that this option
        is without effect if the input file contains no particle identifiers.

        .. _import_file.topology_trajectory_files:

        **Topology and trajectory files**

        Some simulation codes write a *topology* file and separate *trajectory* file. The former contains only static information like the bonding
        between atoms, the atom types, etc., which do not change during a simulation run, while the latter stores the varying data (primarily
        the atomic trajectories). To load such a topology-trajectory pair of files, first read the topology file with
        the :py:func:`!import_file` function, then insert a :py:class:`~ovito.modifiers.LoadTrajectoryModifier` into the returned :py:class:`~ovito.pipeline.Pipeline`
        to also load the trajectory data.

        **Explicit file format specification**

        Normally, OVITO detects the format of the imported file(s) automatically. In rare cases, however, the auto-detection mechanism may fail.
        Then you can explicitly specify the file format to  assume using the ``input_format`` keyword parameter. It must be set to one of the following
        supported format identifiers:
        ``"ca"``, ``"castep/cell"``, ``"castep/md"``, ``"cfg"``, ``"cif"``, ``"dlpoly"``, ``"fhi-aims"``, ``"fhi-aims/log"``, ``"galamost"``,
        ``"gaussian/cube"``, ``"gro"``, ``"gsd/hoomd"``, ``"imd"``, ``"lammps/data"``, ``"lammps/dump"``, ``"lammps/dump/bin"``, ``"lammps/dump/grid"``, ``"lammps/dump/local"``,
        ``"mmcif"``, ``"netcdf/amber"``, ``"obj"``, ``"oxdna"``, ``"paradis"``, ``"parcas"``, ``"pdb"``, ``"quantumespresso"``, ``"reaxff/bonds"``,
        ``"stl"``, ``"vasp"``, ``"vtk/legacy/mesh"``, ``"vtk/pvd"``, ``"vtk/vti/grid"``, ``"vtk/vtm"``, ``"vtk/vtp/mesh"``, ``"vtk/vtp/particles"``,
        ``"vtk/vts/grid"``, ``"xsf"``, ``"xtc"``, ``"xyz"``.

        .. seealso::

            - :ref:`manual:file_formats.input.ase_database`
            - :ref:`manual:file_formats.input.cfg_atomeye`
            - :ref:`manual:file_formats.input.cube`
            - :ref:`manual:file_formats.input.gsd`
            - :ref:`manual:file_formats.input.lammps_data`
            - :ref:`manual:file_formats.input.lammps_dump`
            - :ref:`manual:file_formats.input.lammps_dump_grid`
            - :ref:`manual:file_formats.input.lammps_dump_local`
            - :ref:`manual:file_formats.input.reaxff`
            - :ref:`manual:file_formats.input.xyz`

    """

    if isinstance(location, (str, os.PathLike)):
        location_list = [location]
    elif isinstance(location, collections.Sequence):
        location_list = list(location)
    else:
        raise TypeError("Invalid input file location. Expected str, os.PathLike, or sequence thereof.")
    first_location = location_list[0]

    # Did the caller specify the format of the input file explicitly?
    if 'input_format' in params:
        # Look up the importer class for the registered format name.
        format = params.pop('input_format')
        available_formats = import_file._formatTable
        if not format in available_formats:
            raise ValueError(f"Unknown input format: '{format}'. The supported formats are: {sorted(list(available_formats.keys()))}")

        # Create an instance of the importer class. It will be configured below.
        importer = available_formats[format]()
    else:
        # Auto-detect the file's format if caller did not specify the format explicitly.
        importer = FileImporter.autodetect_format(first_location)
        if not importer:
            raise RuntimeError("Could not detect the file format. The format might not be supported.")

    # Forward user parameters to the file importer object.
    importer_object = importer.delegate if isinstance(importer, PythonScriptFileImporter) else importer
    for key, value in params.items():
        if not hasattr(importer_object, key):
            raise KeyError(f"Invalid keyword parameter. File reader {importer_object!r} doesn't support parameter '{key}'.")
        importer_object.__setattr__(key, value)

    # Import data.
    pipeline = importer.import_file_sequence(location_list)

    try:
        # Block until data has been has been loaded from the file.
        state = pipeline.evaluate_pipeline(0)  # Requesting frame 0 here, because full list of frames is not loaded yet at this point.

        # Raise exception if error occurs during loading.
        if state.status.type == PipelineStatus.Type.Error:
            raise RuntimeError(state.status.text)

        # Block until full list of animation frames is available.
        if isinstance(pipeline.source, FileSource):
            pipeline.source.wait_for_frames_list()

    except:
        # Delete newly created pipeline in case of failure.
        pipeline.delete()
        raise

    return pipeline
ovito.io.import_file = import_file

# This is the table of import file formats used by the import_file() function
# to look up the right importer class for a file format.
# Plugins can register their importer class by inserting a new entry in this dictionary.
import_file._formatTable = {}
