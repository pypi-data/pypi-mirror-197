import collections.abc as collections
import sys
import warnings

from . import Pipeline, Modifier, ModifierInterface
from ..modifiers import PythonScriptModifier
from ..vis import DataVis
from ..nonpublic import PipelineStatus, ModifierApplication

# Implementation of the Pipeline.modifiers collection.
def _Pipeline_modifiers(self):
    """ The sequence of modifiers in the pipeline.

        This list contains any modifiers that are applied to the input data provided by the pipeline's data :py:attr:`source`. You
        can add and remove modifiers as needed using standard Python ``append()`` and ``del`` operations. The
        head of the list represents the beginning of the pipeline, i.e. the first modifier receives the data from the
        data :py:attr:`source`, manipulates it and passes the results on to the second modifier in the list and so forth.

        Example: Adding a new modifier to the end of a data pipeline::

           pipeline.modifiers.append(WrapPeriodicImagesModifier())
    """

    class PipelineModifierList(collections.MutableSequence):
        """ This is a helper class is used for the implementation of the Pipeline.modifiers field. It emulates a
            mutable list of modifiers. The array is generated from the chain (linked list) of ModifierApplication instances
            that make up the pipeline.
        """

        def __init__(self, pipeline):
            """ The constructor stores away a back-pointer to the owning Pipeline. """
            self.pipeline = pipeline

        def _modifierList(self):
            """ Builds an array with all modifiers in the pipeline by traversing the chain of ModifierApplications. """
            mods = []
            obj = self.pipeline.data_provider
            while isinstance(obj, ModifierApplication):
                mods.insert(0, obj.modifier)
                obj = obj.input
            return mods

        def _modAppList(self):
            """ Builds an array with all modifier application in the pipeline. """
            modapps = []
            obj = self.pipeline.data_provider
            while isinstance(obj, ModifierApplication):
                modapps.insert(0, obj)
                obj = obj.input
            return modapps

        def __len__(self):
            """ Determines the total number of modifiers in the pipeline. """
            count = 0
            obj = self.pipeline.data_provider
            while isinstance(obj, ModifierApplication):
                count += 1
                obj = obj.input
            return count

        def __iter__(self):
            """ Returns an iterator that visits all modifiers in the pipeline. """
            return self._modifierList().__iter__()

        def __getitem__(self, i):
            """ Return a modifier from the pipeline by index. """
            return self._modifierList()[i]

        @staticmethod
        def _create_modifier_application(mod):
            # Check if the argument is a valid modifier instance.
            # If it is a Python function, automatically wrap it in a PythonScriptModifier.
            # If it is a Python object implementing the abstract ModifierInterface, automatically wrap it in a PythonScriptModifier.
            # If the caller accidentally passed a Modifier derived class type instead of an instance, automatically instantiate the type.
            # Finally, create and return a ModifierApplication instance for the modifier instance.
            if isinstance(mod, type) and issubclass(mod, Modifier):
                warnings.warn(f"Method expects a modifier instance, not a modifier class type. Did you forget to write parentheses () after {mod.__name__}?", stacklevel=3)
                mod = mod()
            if not isinstance(mod, Modifier):
                if isinstance(mod, ModifierInterface):
                    mod = PythonScriptModifier(delegate=mod)
                elif callable(mod) and not isinstance(mod, type):
                    mod = PythonScriptModifier(function=mod)
                else:
                    raise TypeError("Expected a modifier instance or user-defined modifier function.")
            modapp = mod.create_modifier_application()
            assert(isinstance(modapp, ModifierApplication))
            modapp.modifier = mod
            return modapp

        def __setitem__(self, index, newMod):
            """ Replaces an existing modifier in the pipeline with a new one. """
            modapp = self._create_modifier_application(newMod)
            if isinstance(index, slice):
                raise TypeError("This sequence type does not support slicing.")
            if not isinstance(index, int):
                raise TypeError("Expected integer index")
            if index < 0:
                index += len(self)
            modapplist = self._modAppList()
            if index == len(modapplist) - 1 and index >= 0:
                assert(self.pipeline.data_provider == modapplist[-1])
                self.pipeline.data_provider = modapp
                modapp.input = modapplist[-1].input
            elif 0 <= index < len(modapplist) - 1:
                modapp.input = modapplist[index].input
                modapplist[index + 1].input = modapp
            else:
                raise IndexError("List index is out of range.")
            modapp.modifier.initialize_modifier(modapp, None)

        def __delitem__(self, index):
            """ Removes a modifier from the pipeline by index. """
            if isinstance(index, slice):
                raise TypeError("This sequence type does not support slicing.")
            if not isinstance(index, int):
                raise TypeError("Expected integer index")
            if index < 0:
                index += len(self)
            modapplist = self._modAppList()
            if index >= 0 and index == len(modapplist) - 1:
                assert(self.pipeline.data_provider == modapplist[-1])
                self.pipeline.data_provider = modapplist[-1].input
            elif 0 <= index < len(modapplist) - 1:
                modapplist[index + 1].input = modapplist[index].input
            else:
                raise IndexError("List index is out of range.")

        def insert(self, index, mod):
            """ Inserts a new modifier into the pipeline at a given position. """
            if not isinstance(index, int):
                raise TypeError("Expected integer index")
            if index < 0:
                index += len(self)
            modapplist = self._modAppList()
            modapp = self._create_modifier_application(mod)
            if index == len(modapplist) and index >= 0:
                assert(self.pipeline.data_provider == modapplist[-1])
                self.pipeline.data_provider = modapp
                modapp.input = modapplist[-1]
            elif 0 <= index <= len(modapplist) - 1:
                modapp.input = modapplist[index].input
                modapplist[index].input = modapp
            else:
                raise IndexError("List index is out of range.")
            modapp.modifier.initialize_modifier(modapp, None)

        def append(self, mod):
            """ Inserts a new modifier at the end of the pipeline. """
            # Automatically wrap Python methods in a PythonScriptModifier object.
            modapp = self._create_modifier_application(mod)
            modapp.input = self.pipeline.data_provider
            self.pipeline.data_provider = modapp
            modapp.modifier.initialize_modifier(modapp, None)

        def clear(self):
            """ Removes all modifiers from the pipeline. """
            self.pipeline.data_provider = self.pipeline.source
            assert len(self) == 0

        def __str__(self):
            return str(self._modifierList())

    return PipelineModifierList(self)
Pipeline.modifiers = property(_Pipeline_modifiers)

def _Pipeline_compute(self, frame = None):
    """ Computes and returns the results of this data pipeline.

        This method requests an evaluation of the pipeline and blocks while the input data is being obtained from the
        data :py:attr:`source` and all modifiers are applied to the data. If you invoke the :py:meth:`!compute` method repeatedly
        without changing the pipeline between calls, the method may serve subsequent requests by immediately returning a cached pipeline output.

        The optional *frame* parameter specifies the animation time at which the pipeline should be evaluated. Frame numbering starts at 0.
        If you don't specify a frame number, the current time slider position of OVITO is used; or frame 0 when execution doesn't take place in an interactive OVITO session.

        The :py:meth:`!compute` method raises a ``RuntimeError`` if the pipeline could not be successfully evaluated for some reason.
        This may happen due to invalid modifier settings or file I/O errors, for example.

        :param int frame: The animation frame number at which the pipeline should be evaluated.
        :returns: A :py:class:`~ovito.data.DataCollection` produced by the data pipeline.

        .. note::

           This method creates a static snapshot of the results of the current pipeline.
           The returned :py:class:`~ovito.data.DataCollection` will *not* reflect any changes you subsequently make
           to the pipeline or the modifiers. You have to invoke :py:meth:`!compute` again if you want updated results.

        .. note::

           The returned :py:class:`~ovito.data.DataCollection` behaves like an independent copy of the pipeline's output data.
           If you make changes to the objects in the :py:class:`~ovito.data.DataCollection`, the changes will *not*
           be visible to the modifiers within the pipeline nor will they be persistent, i.e., subsequent calls to :py:meth:`!compute`
           will *not* produce data collections containing the same changes.

           If your intention is to change the data before it gets passed to the modifiers in the pipeline, insert a
           :ref:`user-defined modifier function <writing_custom_modifiers>` into the pipeline, which lets you manipulate the
           :py:class:`~ovito.data.DataCollection` before subsequent modifiers in the downstream pipeline see it.

    """
    state = self.evaluate_pipeline(frame)
    if state.status.type == PipelineStatus.Type.Error:
        raise RuntimeError(f"Data pipeline failure: {state.status.text}")
    if not state.data:
        raise RuntimeError("Data pipeline did not yield any output DataCollection.")

    return state.mutable_data
Pipeline.compute = _Pipeline_compute
